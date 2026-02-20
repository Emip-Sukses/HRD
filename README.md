# HRD Application (v2.0 - Production Ready)

Aplikasi manajemen absensi karyawan berbasis Django dengan arsitektur modern, keamanan tinggi, dan antarmuka premium.

## Fitur Utama
- **Absensi Real-time**: Mencatat jam masuk dan pulang dengan presisi.
- **Glassmorphism UI**: Desain antarmuka modern, responsif, dan elegan.
- **Role Management**: Pemisahan akses antara Karyawan dan Admin HR.
- **Secure Backend**: Menggunakan PostgreSQL 17, Environment Variables, dan Gunicorn.

## Teknologi
- **Backend**: Django 6.0, Python 3.12
- **Database**: PostgreSQL 17 (via `psycopg2-binary`)
- **Frontend**: Bootstrap 5 + Custom Glassmorphism CSS
- **Server**: Gunicorn + Whitenoise

## Instalasi & Menjalankan
1. **Persiapan Database**: Pastikan PostgreSQL berjalan di port 5432.
2. **Setup Lingkungan**:
   ```bash
   cp .env.example .env  # (Otomatis dibuat saat instalasi)
   ./venv/bin/pip install -e .
   ```
3. **Jalankan Aplikasi**:
   Gunakan script otomatis untuk memulai server:
   ```bash
   ./start_hrd.sh
   ```
   Aplikasi akan berjalan di `http://0.0.0.0:8010`.

## Akun Default
- **Superuser (Admin)**:
  - Username: `admin`
  - Password: `adminpassword123`
- **Karyawan**: Buat melalui Admin Panel atau registrasi manual.

## Struktur Project
- `hrd_app/`: Core logic aplikasi.
- `hrd_project/`: Konfigurasi Django.
- `static/`: File statis (CSS/JS) yang dikelola Whitenoise.
- `gunicorn_start.sh`: Konfigurasi server produksi.
