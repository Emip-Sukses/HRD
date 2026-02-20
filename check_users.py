import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrd_project.settings')
django.setup()

from django.contrib.auth.models import User
from hrd_app.models import Employee

print("--- DAFTAR USER & KARYAWAN ---")
print(f"{'USERNAME':<20} | {'FULL NAME':<30} | {'IS STAFF':<10} | {'HAS EMPLOYEE PROFILE'}")
print("-" * 80)

users = User.objects.all()
for user in users:
    try:
        emp = user.employee
        has_emp = f"Yes (NIK: {emp.employee_id})"
    except:
        has_emp = "No"
    
    print(f"{user.username:<20} | {user.get_full_name():<30} | {str(user.is_staff):<10} | {has_emp}")

print("\n--- DAFTAR KARYAWAN TANPA USER ---")
employees = Employee.objects.filter(user__isnull=True)
if employees.exists():
    for emp in employees:
        print(f"NIK: {emp.employee_id} - {emp.name}")
else:
    print("Tidak ada.")
