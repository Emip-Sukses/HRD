from django.contrib import admin
from .models import Employee, Department, Attendance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    # Kolom yang muncul di daftar admin
    list_display = ('employee_id', 'name', 'department', 'position', 'joined_date')
    # Fitur pencarian sesuai poin 1.f
    search_fields = ('name', 'employee_id')
    # Filter samping sesuai poin 1.b
    list_filter = ('department', 'position')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('date', 'status')