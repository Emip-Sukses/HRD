import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrd_project.settings')
django.setup()

from django.contrib.auth.models import User
from hrd_app.models import Employee

print("--- FIXING USER-EMPLOYEE LINKS ---")

# Cari karyawan yang belum punya user
employees = Employee.objects.filter(user__isnull=True)

for emp in employees:
    username = emp.employee_id.lower()
    print(f"Checking Employee: {emp.name} (NIK: {username})")
    
    # Cek apakah user dengan username ini sudah ada
    try:
        user = User.objects.get(username=username)
        print(f"  -> User '{username}' ditemukan. Linking...")
        
        # Link user ke employee
        emp.user = user
        emp.save()
        print(f"  -> Linked successfully!")
        
        # Reset password to be sure
        user.set_password("password123")
        user.save()
        print(f"  -> Password reset to 'password123'")
        
    except User.DoesNotExist:
        print(f"  -> User '{username}' tidak ditemukan. Creating new user...")
        user = User.objects.create_user(
            username=username,
            password="password123",
            first_name=emp.name.split()[0]
        )
        emp.user = user
        emp.save()
        print(f"  -> User created and linked.")

print("\n--- SELESAI ---")
