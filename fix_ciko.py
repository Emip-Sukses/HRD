import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrd_project.settings')
django.setup()

from django.contrib.auth.models import User
from hrd_app.models import Employee

print("--- FIXING CIKO PROFILE ---")

# 1. Cari Karyawan bernama Ciko
try:
    ciko_emp = Employee.objects.get(name__icontains="Ciko")
    print(f"Found Employee: {ciko_emp.name} (NIK: {ciko_emp.employee_id})")
    print(f"Current User Linked: {ciko_emp.user}")

    # 2. Cari User Ciko09
    try:
        ciko_user = User.objects.get(username="Ciko09")
        print(f"Found User Target: {ciko_user.username}")

        # 3. Pindahkan Link
        ciko_emp.user = ciko_user
        ciko_emp.save()
        print(f"✅ SUCCESS: Employee '{ciko_emp.name}' now linked to User '{ciko_user.username}'")

    except User.DoesNotExist:
        print("❌ ERROR: User 'Ciko09' not found!")

except Employee.DoesNotExist:
    print("❌ ERROR: Employee matching 'Ciko' not found!")

print("\n--- SELESAI ---")
