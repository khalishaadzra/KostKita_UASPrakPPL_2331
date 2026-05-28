from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from dateutil.relativedelta import relativedelta
from .models import Kamar, Pengajuan, BuktiBayar, HARGA_MAP
from .forms import KamarForm, PengajuanForm, BuktiBayarForm

# ─── PUBLIC ──────────────────────────────────────────────────

def landing(request):
    kamar_tersedia = Kamar.objects.filter(status='tersedia').count()
    kamar_terisi = Kamar.objects.filter(status='terisi').count()
    kamar_unggulan = Kamar.objects.filter(status='tersedia')[:3]
    return render(request, 'public/landing.html', {
        'kamar_tersedia': kamar_tersedia,
        'kamar_terisi': kamar_terisi,
        'kamar_unggulan': kamar_unggulan,
    })

def daftar_kamar(request):
    kamar = Kamar.objects.all().order_by('nomor')
    return render(request, 'public/daftar_kamar.html', {'kamar': kamar})

def detail_kamar(request, pk):
    kamar = get_object_or_404(Kamar, pk=pk)
    return render(request, 'public/detail_kamar.html', {'kamar': kamar})

def ajukan_sewa(request, kamar_id):
    kamar = get_object_or_404(Kamar, pk=kamar_id)
    if kamar.status == 'terisi':
        messages.error(request, 'Kamar ini sudah terisi.')
        return redirect('detail_kamar', pk=kamar_id)
    if request.method == 'POST':
        form = PengajuanForm(request.POST, request.FILES)
        if form.is_valid():
            pengajuan = form.save(commit=False)
            pengajuan.kamar = kamar
            pengajuan.save()
            messages.success(request, f'Pengajuan berhasil! ID kamu: #{pengajuan.pk}. Simpan ID ini untuk cek status.')
            return redirect('cek_status', pengajuan_id=pengajuan.pk)
    else:
        form = PengajuanForm()
    return render(request, 'public/ajukan_sewa.html', {'form': form, 'kamar': kamar, 'harga_map': HARGA_MAP})

def upload_bukti(request, pengajuan_id):
    pengajuan = get_object_or_404(Pengajuan, pk=pengajuan_id)
    if pengajuan.status != 'disetujui':
        messages.error(request, 'Pengajuan belum disetujui admin.')
        return redirect('cek_status', pengajuan_id=pengajuan_id)
    if request.method == 'POST':
        form = BuktiBayarForm(request.POST, request.FILES)
        if form.is_valid():
            bukti = form.save(commit=False)
            bukti.pengajuan = pengajuan
            bukti.save()
            pengajuan.status = 'menunggu_verifikasi'
            pengajuan.save()
            messages.success(request, 'Bukti bayar berhasil diupload! Tunggu verifikasi admin.')
            return redirect('cek_status', pengajuan_id=pengajuan_id)
    else:
        form = BuktiBayarForm()
    return render(request, 'public/upload_bukti.html', {'form': form, 'pengajuan': pengajuan})

def cek_status(request, pengajuan_id):
    pengajuan = get_object_or_404(Pengajuan, pk=pengajuan_id)
    return render(request, 'public/cek_status.html', {'pengajuan': pengajuan})

def cek_status_form(request):
    if request.method == 'POST':
        pengajuan_id = request.POST.get('pengajuan_id')
        try:
            return redirect('cek_status', pengajuan_id=int(pengajuan_id))
        except:
            messages.error(request, 'ID pengajuan tidak ditemukan.')
    return render(request, 'public/cek_status_form.html')

# ─── AUTH ────────────────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Username atau password salah, atau bukan akun admin.')
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    logout(request)
    return redirect('landing')

# ─── DASHBOARD ───────────────────────────────────────────────

@login_required
def dashboard(request):
    pengajuan_baru = Pengajuan.objects.filter(status='menunggu').count()
    menunggu_verifikasi = BuktiBayar.objects.filter(status='menunggu').count()
    penyewa_aktif = Pengajuan.objects.filter(status='berhasil')
    total_pemasukan = sum(p.total_harga for p in Pengajuan.objects.filter(status='berhasil'))
    context = {
        'total_kamar': Kamar.objects.count(),
        'kamar_tersedia': Kamar.objects.filter(status='tersedia').count(),
        'kamar_terisi': Kamar.objects.filter(status='terisi').count(),
        'pengajuan_baru': pengajuan_baru,
        'menunggu_verifikasi': menunggu_verifikasi,
        'penyewa_aktif': penyewa_aktif.count(),
        'total_pemasukan': total_pemasukan,
        'pengajuan_terbaru': Pengajuan.objects.order_by('-tanggal_ajuan')[:5],
        'bukti_terbaru': BuktiBayar.objects.filter(status='menunggu').order_by('-tanggal_upload')[:5],
    }
    return render(request, 'admin_panel/dashboard.html', context)

# ─── KAMAR ───────────────────────────────────────────────────

@login_required
def kamar_list(request):
    kamar = Kamar.objects.all().order_by('nomor')
    return render(request, 'admin_panel/kamar_list.html', {'kamar': kamar})

@login_required
def kamar_tambah(request):
    form = KamarForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Kamar berhasil ditambahkan!')
        return redirect('kamar_list')
    return render(request, 'admin_panel/kamar_form.html', {'form': form, 'title': 'Tambah Kamar'})

@login_required
def kamar_edit(request, pk):
    kamar = get_object_or_404(Kamar, pk=pk)
    form = KamarForm(request.POST or None, request.FILES or None, instance=kamar)
    if form.is_valid():
        form.save()
        messages.success(request, 'Kamar berhasil diupdate!')
        return redirect('kamar_list')
    return render(request, 'admin_panel/kamar_form.html', {'form': form, 'title': 'Edit Kamar'})

@login_required
def kamar_hapus(request, pk):
    kamar = get_object_or_404(Kamar, pk=pk)
    if request.method == 'POST':
        kamar.delete()
        messages.success(request, 'Kamar berhasil dihapus!')
        return redirect('kamar_list')
    return render(request, 'admin_panel/konfirmasi_hapus.html', {'obj': kamar, 'nama': f'Kamar {kamar.nomor}', 'back_url': 'kamar_list'})

# ─── PENGAJUAN ───────────────────────────────────────────────

@login_required
def pengajuan_list(request):
    status_filter = request.GET.get('status', '')
    pengajuan = Pengajuan.objects.all().order_by('-tanggal_ajuan')
    if status_filter:
        pengajuan = pengajuan.filter(status=status_filter)
    return render(request, 'admin_panel/pengajuan_list.html', {
        'pengajuan': pengajuan,
        'status_filter': status_filter,
    })

@login_required
def pengajuan_detail(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    bukti = BuktiBayar.objects.filter(pengajuan=pengajuan).last()
    return render(request, 'admin_panel/pengajuan_detail.html', {
        'pengajuan': pengajuan,
        'bukti': bukti,
    })

@login_required
def pengajuan_setujui(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    pengajuan.status = 'disetujui'
    pengajuan.save()
    messages.success(request, f'Pengajuan {pengajuan.nama} disetujui! Menunggu pembayaran.')
    return redirect('pengajuan_list')

@login_required
def pengajuan_tolak(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    pengajuan.status = 'ditolak'
    pengajuan.save()
    messages.success(request, f'Pengajuan {pengajuan.nama} ditolak.')
    return redirect('pengajuan_list')

# ─── PENGAJUAN ───────────────────────────────────────────────

@login_required
def pengajuan_list(request):
    status_filter = request.GET.get('status', '')
    pengajuan = Pengajuan.objects.all().order_by('-tanggal_ajuan')
    if status_filter:
        pengajuan = pengajuan.filter(status=status_filter)
    return render(request, 'admin_panel/pengajuan_list.html', {
        'pengajuan': pengajuan,
        'status_filter': status_filter,
    })

@login_required
def pengajuan_detail(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    bukti = BuktiBayar.objects.filter(pengajuan=pengajuan).last()
    return render(request, 'admin_panel/pengajuan_detail.html', {
        'pengajuan': pengajuan,
        'bukti': bukti,
    })

@login_required
def pengajuan_setujui(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    pengajuan.status = 'disetujui'
    pengajuan.save()
    messages.success(request, f'Pengajuan {pengajuan.nama} disetujui! Menunggu pembayaran.')
    return redirect('pengajuan_list')

@login_required
def pengajuan_tolak(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    pengajuan.status = 'ditolak'
    pengajuan.save()
    messages.success(request, f'Pengajuan {pengajuan.nama} ditolak.')
    return redirect('pengajuan_list')

@login_required
def pengajuan_selesai(request, pk):
    pengajuan = get_object_or_404(Pengajuan, pk=pk)
    kamar = pengajuan.kamar
    
    # 1. Ubah status pengajuan menjadi selesai
    pengajuan.status = 'selesai'
    pengajuan.save()
    
    # 2. Kembalikan status kamar menjadi tersedia
    if kamar:
        kamar.status = 'tersedia'
        kamar.save()
        
    messages.success(request, f'Sewa untuk {pengajuan.nama} telah selesai. Kamar {kamar.nomor} kini tersedia kembali.')
    return redirect('penyewa_list')

# ─── BUKTI BAYAR ─────────────────────────────────────────────

@login_required
def bukti_list(request):
    bukti = BuktiBayar.objects.all().order_by('-tanggal_upload')
    return render(request, 'admin_panel/bukti_list.html', {'bukti': bukti})

@login_required
def bukti_verifikasi(request, pk):
    bukti = get_object_or_404(BuktiBayar, pk=pk)
    bukti.status = 'verified'
    bukti.save()
    pengajuan = bukti.pengajuan
    pengajuan.status = 'berhasil'
    pengajuan.tanggal_mulai = date.today()
    try:
        pengajuan.tanggal_selesai = date.today() + relativedelta(months=pengajuan.durasi)
    except:
        from datetime import timedelta
        pengajuan.tanggal_selesai = date.today() + timedelta(days=30 * pengajuan.durasi)
    pengajuan.save()
    pengajuan.kamar.status = 'terisi'
    pengajuan.kamar.save()
    messages.success(request, f'Pembayaran {pengajuan.nama} terverifikasi! Kamar {pengajuan.kamar.nomor} sekarang terisi.')
    return redirect('bukti_list')

@login_required
def bukti_tolak(request, pk):
    bukti = get_object_or_404(BuktiBayar, pk=pk)
    bukti.status = 'ditolak'
    bukti.save()
    bukti.pengajuan.status = 'disetujui'
    bukti.pengajuan.save()
    messages.success(request, 'Bukti bayar ditolak. Penyewa perlu upload ulang.')
    return redirect('bukti_list')

# ─── PENYEWA AKTIF ───────────────────────────────────────────

@login_required
def penyewa_list(request):
    penyewa = Pengajuan.objects.filter(status='berhasil').order_by('kamar__nomor')
    riwayat = Pengajuan.objects.filter(status='selesai').order_by('-tanggal_ajuan')
    return render(request, 'admin_panel/penyewa_list.html', {
        'penyewa': penyewa,
        'riwayat': riwayat,
    })