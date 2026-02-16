from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# 1.b Manajemen Departemen
class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 1.a Manajemen Karyawan
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.name}"

    # Fungsi pembantu untuk absen hari ini
    def get_today_attendance(self):
        return self.attendance_set.filter(date=timezone.now().date()).first()

# 1.c Manajemen Kehadiran
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Hadir')

    def __str__(self):
        return f"{self.employee.name} - {self.date}"