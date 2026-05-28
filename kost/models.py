from django.db import models

DURASI_CHOICES = [
    (1, '1 Bulan - Rp 1.000.000'),
    (6, '6 Bulan - Rp 6.000.000'),
    (12, '12 Bulan - Rp 12.000.000'),
]

HARGA_MAP = {1: 1000000, 6: 6000000, 12: 12000000}

class Kamar(models.Model):
    STATUS_CHOICES = [('tersedia', 'Tersedia'), ('terisi', 'Terisi')]
    nomor = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='tersedia')
    foto = models.ImageField(upload_to='kamar/', blank=True, null=True)
    lantai = models.IntegerField(default=1)

    def __str__(self):
        return f"Kamar {self.nomor}"


class Pengajuan(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu Review'),
        ('disetujui', 'Disetujui - Menunggu Pembayaran'),
        ('menunggu_verifikasi', 'Menunggu Verifikasi Bayar'),
        ('berhasil', 'Berhasil'),
        ('ditolak', 'Ditolak'),
        ('selesai', 'Selesai'),
    ]
    JENIS_KELAMIN_CHOICES = [('L', 'Laki-laki'), ('P', 'Perempuan')]

    kamar = models.ForeignKey(Kamar, on_delete=models.CASCADE)
    # Data diri
    nama = models.CharField(max_length=100)
    umur = models.IntegerField()
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN_CHOICES)
    no_hp = models.CharField(max_length=15)
    scan_ktp = models.ImageField(upload_to='ktp/')
    # Sewa
    durasi = models.IntegerField(choices=DURASI_CHOICES, default=1)
    total_harga = models.BigIntegerField(default=0)
    tanggal_mulai = models.DateField(null=True, blank=True)
    tanggal_selesai = models.DateField(null=True, blank=True)
    # Status
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='menunggu')
    tanggal_ajuan = models.DateTimeField(auto_now_add=True)
    catatan_admin = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        self.total_harga = HARGA_MAP.get(self.durasi, 0)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nama} - Kamar {self.kamar.nomor}"


class BuktiBayar(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu Verifikasi'),
        ('verified', 'Verified'),
        ('ditolak', 'Ditolak'),
    ]
    pengajuan = models.ForeignKey(Pengajuan, on_delete=models.CASCADE)
    foto_bukti = models.ImageField(upload_to='bukti_bayar/')
    catatan = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='menunggu')
    tanggal_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bukti - {self.pengajuan.nama}"