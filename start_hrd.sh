#!/bin/bash
set -e

APP_DIR="/opt/services/hrd"
VENV_ACTIVATE="$APP_DIR/venv/bin/activate"

echo "🚀 Memulai Pembaruan Sistem HRD..."

# 1. Pastikan PostgreSQL Berjalan
echo "-> Memastikan Database PostgreSQL aktif..."
if sudo -n true 2>/dev/null; then
    sudo service postgresql start > /dev/null 2>&1 || true
else
    echo "⚠️  Sudo password mungkin diperlukan untuk memulai PostgreSQL."
    sudo service postgresql start || true
fi

# 2. Aktivasi Virtual Environment
echo "-> Mengaktifkan Virtual Environment..."
source $VENV_ACTIVATE

# 3. Jalankan Migrasi Database
echo "-> Menjalankan Migrasi Database..."
python manage.py migrate --noinput

# 4. Kumpulkan File Statis (CSS/JS/Images)
echo "-> Mengumpulkan File Statis (Whitenoise)..."
python manage.py collectstatic --noinput

# 5. Buat Superuser (jika belum ada)
echo "-> Memastikan Admin User..."
python create_superuser.py

# 6. Jalankan Server Gunicorn
echo "-> Menjalankan Server Aplikasi (Port 8000)..."
exec ./gunicorn_start.sh
