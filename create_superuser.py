import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrd_project.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
password = 'adminpassword123'
email = 'admin@hrd.local'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ Superuser created.")
    print(f"Username: {username}")
    print(f"Password: {password}")
else:
    print("ℹ️ Superuser 'admin' already exists.")
