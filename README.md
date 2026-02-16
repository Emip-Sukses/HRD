# HRD Application

Aplikasi manajemen absensi karyawan berbasis Django.

## Fitur
- Absen masuk dan pulang karyawan.
- Rekap absensi (khusus admin).

## Instalasi
1. Clone repository ini.
2. Buat virtual environment: `python -m venv venv`.
3. Install dependencies: `./venv/bin/pip install -e .`.
4. Jalankan migrasi: `./venv/bin/python manage.py migrate`.
5. Jalankan server: `./venv/bin/python manage.py runserver 0.0.0.0:8000`.
