# 🏠 KostKita - Aplikasi Manajemen Kost

Aplikasi web manajemen kost berbasis Django untuk mengelola kamar, penyewa, dan pembayaran.

## Teknologi
- **Backend**: Django 6.0 (Python)
- **Database**: SQLite
- **Frontend**: HTML, Bootstrap 5, CSS custom

## Fitur
### Publik
- Landing page dengan info kost & fasilitas
- Lihat daftar & detail kamar
- Ajukan sewa dengan upload KTP
- Pilih durasi sewa (1, 6, 12 bulan)
- Upload bukti pembayaran
- Cek status pengajuan via ID

### Admin
- Dashboard statistik kamar & pemasukan
- CRUD kamar
- Kelola pengajuan (setujui/tolak)
- Verifikasi bukti pembayaran
- Data penyewa aktif & riwayat sewa

## Instalasi
1. Clone repo
```bash
   git clone https://github.com/USERNAME/kostkita.git
   cd kostkita
```
2. Buat virtual environment
```bash
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies
```bash
   pip install django pillow python-dateutil
```
4. Migrasi database
```bash
   python manage.py migrate
```
5. Buat akun admin
```bash
   python manage.py createsuperuser
```
6. Jalankan server
```bash
   python manage.py runserver
```
7. Buka browser: `http://127.0.0.1:8000`

## Akun Admin
- URL: `/admin-panel/login/`
- Login dengan akun superuser yang dibuat di langkah 5