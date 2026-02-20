# AGENTS.md - HRD Service (v2.0)

Standar Operasional Prosedur (SOP) untuk layanan HRD Modern.

## Context
- **Aplikasi**: Django HRD App (Glassmorphism & Secure Backend)
- **CWD**: `/opt/services/hrd`
- **Venv**: `/opt/services/hrd/venv`
- **Database**: PostgreSQL 17 (`hrd_db` on localhost:5432)
- **Server**: Gunicorn + Whitenoise

## Cara Menjalankan (Production Mode)
Gunakan script wrapper yang telah disiapkan untuk memastikan environment, database, dan statis file termuat dengan benar:
```bash
./start_hrd.sh
```
Script ini otomatis:
1. Memulai PostgreSQL Service.
2. Mengaktifkan Virtualenv.
3. Menjalankan Migrasi Database.
4. Mengumpulkan Static Files (Whitenoise).
5. Membuat Admin User (`admin` / `adminpassword123`).
6. Menjalankan Gunicorn pada port `8000`.

## Struktur Proyek Baru
- `hrd_app/static/hrd_app/css/style.css`: Core styling (Glassmorphism).
- `.env`: Konfigurasi rahasia (SECRET_KEY, DB config).
- `gunicorn_start.sh`: Script peluncur Gunicorn.
- `create_db.py`: Utilitas inisialisasi database PostgreSQL.

## Maintenance
- **Database**: Gunakan `psql -d hrd_db` untuk akses langsung.
- **Log**: Output server muncul langsung di terminal saat menjalankan `./start_hrd.sh`.
- **Update**: Setelah perubahan kode, restart script `./start_hrd.sh`.
