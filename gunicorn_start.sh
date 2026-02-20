#!/bin/bash

# Pastikan script berhenti jika terjadi error
set -e

# Nama aplikasi
NAME="hrd_app"
# Direktori proyek
DJANGODIR=/opt/services/hrd
# User/Group yang akan menjalankan (sesuaikan dengan system user)
USER=miftah
GROUP=miftah
# Jumlah worker (biasanya 2 * CPU + 1)
NUM_WORKERS=3
# Modul WSGI Django
DJANGO_WSGI_MODULE=hrd_project.wsgi

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source venv/bin/activate
export PYTHONPATH=$DJANGODIR:$PYTHONPATH


# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --user=$USER --group=$GROUP \
  --bind=0.0.0.0:8010 \
  --log-level=info \
  --log-file=-
