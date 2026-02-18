from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Model Departemen: Mengelompokkan karyawan berdasarkan divisi kerja
class Department(models.Model):
    """
    Menyimpan data departemen/divisi dalam perusahaan.
    """
    name = models.CharField(max_length=100, verbose_name="Nama Departemen")
    description = models.TextField(blank=True, verbose_name="Deskripsi")

    def __str__(self):
        # Mengembalikan nama departemen saat objek direpresentasikan sebagai string
        return self.name

    class Meta:
        verbose_name = "Departemen"
        verbose_name_plural = "Daftar Departemen"

# Model Karyawan: Menyimpan informasi detail setiap staf
class Employee(models.Model):
    """
    Ekstensi dari model User bawaan Django untuk menyimpan profil tambahan karyawan.
    Setiap Karyawan terhubung satu-ke-satu dengan akun User.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Akun User")
    name = models.CharField(max_length=200, verbose_name="Nama Lengkap")
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Nomor Induk Karyawan (NIK)")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, verbose_name="Departemen")
    position = models.CharField(max_length=100, verbose_name="Jabatan")
    address = models.TextField(verbose_name="Alamat")
    phone = models.CharField(max_length=15, verbose_name="No. Telepon")
    joined_date = models.DateField(auto_now_add=True, verbose_name="Tanggal Bergabung")
    
    def __str__(self):
        # Format string: "NIK - Nama"
        return f"{self.employee_id} - {self.name}"

    def get_today_attendance(self):
        """
        Mengambil data absensi karyawan untuk hari ini.
        Jika tidak ada, mengembalikan None.
        """
        return self.attendance_set.filter(date=timezone.now().date()).first()

    class Meta:
        verbose_name = "Karyawan"
        verbose_name_plural = "Daftar Karyawan"

# Model Kehadiran: Mencatat log masuk dan pulang karyawan
class Attendance(models.Model):
    """
    Mencatat data harian absensi: jam masuk, jam pulang, dan status.
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Karyawan")
    date = models.DateField(auto_now_add=True, verbose_name="Tanggal")
    check_in = models.TimeField(null=True, blank=True, verbose_name="Jam Masuk")
    check_out = models.TimeField(null=True, blank=True, verbose_name="Jam Pulang")
    # Status default adalah 'Hadir', bisa dikembangkan untuk 'Sakit', 'Izin', dsb.
    status = models.CharField(max_length=20, default='Hadir', verbose_name="Status")

    def __str__(self):
        # Representasi string untuk log absensi
        return f"{self.employee.name} - {self.date}"

    class Meta:
        verbose_name = "Kehadiran"
        verbose_name_plural = "Log Kehadiran"
        # Memastikan satu karyawan hanya punya satu baris absensi per hari
        unique_together = ('employee', 'date')