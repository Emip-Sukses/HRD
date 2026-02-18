from django.contrib import admin
from .models import Employee, Department, Attendance

# Konfigurasi Admin untuk Departemen
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Manajemen departemen di panel admin.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)

# Konfigurasi Admin untuk Karyawan
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Manajemen data karyawan dengan fitur filter dan pencarian.
    """
    # Menampilkan kolom-kolom penting di tabel daftar
    list_display = ('employee_id', 'name', 'department', 'position', 'joined_date')
    # Memungkinkan pencarian berdasarkan nama dan NIK
    search_fields = ('name', 'employee_id')
    # Filter samping berdasarkan departemen dan jabatan
    list_filter = ('department', 'position')
    # Mempermudah pemilihan akun user
    raw_id_fields = ('user',)

# Konfigurasi Admin untuk Kehadiran (Logs)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Log harian kehadiran karyawan.
    """
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    # Filter berdasarkan tanggal dan status kehadiran
    list_filter = ('date', 'status', 'employee__department')
    # Pencarian berdasarkan nama karyawan
    search_fields = ('employee__name', 'employee__employee_id')
    # Urutan default: terbaru di atas
    ordering = ('-date', '-check_in')