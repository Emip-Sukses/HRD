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
    actions_on_top = True
    actions_selection_counter = True
    
    # Aksi kustom: Reset Password
    actions = ['reset_password_to_default']
    
    @admin.action(description="Reset password ke default (password123)")
    def reset_password_to_default(self, request, queryset):
        """
        Aksi untuk mereset password user yang terhubung menjadi 'password123'
        """
        success_count = 0
        for employee in queryset:
            if employee.user:
                employee.user.set_password('password123')
                employee.user.save()
                success_count += 1
        
        self.message_user(request, f"✅ Berhasil! {success_count} akun karyawan telah direset passwordnya menjadi 'password123'.")

# Konfigurasi Admin untuk Kehadiran (Logs)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Log harian kehadiran karyawan.
    """
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status', 'location_info')
    # Filter berdasarkan tanggal dan status kehadiran
    list_filter = ('date', 'status', 'employee__department')
    # Pencarian berdasarkan nama karyawan
    search_fields = ('employee__name', 'employee__employee_id')
    # Urutan default: terbaru di atas
    ordering = ('-date', '-check_in')

    @admin.display(description="Info Lokasi (Lat,Lon)")
    def location_info(self, obj):
        """
        Menampilkan koordinat masuk dalam satu kolom di daftar tabel.
        """
        if obj.lat_in and obj.lon_in:
            return f"{obj.lat_in:.4f}, {obj.lon_in:.4f}"
        return "-"