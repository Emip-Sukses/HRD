# AGENTS.md - HRD Service

SOP operasional untuk layanan HRD.

## Context
- **Aplikasi**: Django HRD App (Absensi)
- **CWD**: `/opt/services/hrd`
- **Venv**: `/opt/services/hrd/venv` (Sesuai struktur yang ada)
- **Database**: SQLite3 (`db.sqlite3`)

## Cara Menjalankan
### Development Mode
```bash
/opt/services/hrd/venv/bin/python manage.py runserver 0.0.0.0:8000
```

## Struktur Proyek
- `hrd_project/`: Konfigurasi Django.
- `hrd_app/`: Konten aplikasi (views, models, templates).
- `manage.py`: Utilitas manajemen Django.

## Maintenance
- Pastikan venv aktif saat menginstall package baru.
- Lakukan migrasi jika ada perubahan pada `hrd_app/models.py`.
