from django.shortcuts import render, redirect
from .models import Employee, Attendance
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 

def login_karyawan(request):
    """
    View untuk menangani login khusus karyawan.
    Admin tidak diperbolehkan login melalui halaman ini.
    """
    # Jika sudah login, langsung lempar ke halaman utama
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Otentikasi user menggunakan backend Django
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Memastikan hanya non-staff (karyawan biasa) yang bisa login di sini
            if not user.is_staff:
                login(request, user)
                messages.success(request, f"Selamat datang kembali, {user.first_name or user.username}!")
                return redirect('index')
            else:
                # Admin diarahkan ke portal manajemen resmi
                messages.error(request, "Akses ditolak: Admin harus login melalui portal /admin/")
        else:
            messages.error(request, "Kredensial salah: Username atau Password tidak valid.")
    
    return render(request, 'hrd_app/login_karyawan.html')

@login_required
def user_logout(request):
    """
    View untuk menangani pemutusan sesi (logout) karyawan.
    """
    logout(request)
    messages.success(request, "Anda telah berhasil keluar dari sistem.")
    return redirect('login_karyawan')

@login_required
def index(request):
    """
    Dashboard utama karyawan untuk melakukan absensi masuk dan pulang.
    """
    today = timezone.now().date()
    
    # Mencari data profil karyawan yang terhubung dengan akun user
    # Menggunakan select_related untuk mengoptimalkan pengambilan data departemen
    employee = None
    try:
        employee = Employee.objects.select_related('department').get(user=request.user)
    except Employee.DoesNotExist:
        messages.error(request, "Profil karyawan tidak ditemukan. Silakan hubungi bagian HRD.")
    
    # Menangani aksi tombol Absen Masuk atau Absen Pulang
    if request.method == "POST" and employee:
        aksi = request.POST.get('aksi')
        
        if aksi == "masuk":
            # get_or_create memastikan tidak ada duplikasi data absensi di hari yang sama
            obj, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={'check_in': timezone.now().time()}
            )
            if created:
                messages.success(request, f"Absen masuk berhasil pada pukul {obj.check_in.strftime('%H:%M')}. Selamat bekerja!")
            else:
                messages.warning(request, "Anda sudah tercatat melakukan absen masuk hari ini.")
                
        elif aksi == "pulang":
            # Mencari data absensi hari ini yang jam pulangnya masih kosong
            absen = Attendance.objects.filter(employee=employee, date=today).first()
            if absen:
                if not absen.check_out:
                    absen.check_out = timezone.now().time()
                    absen.save()
                    messages.info(request, f"Absen pulang berhasil pada pukul {absen.check_out.strftime('%H:%M')}. Hati-hati di jalan!")
                else:
                    messages.warning(request, "Anda sudah tercatat melakukan absen pulang hari ini.")
            else:
                messages.error(request, "Gagal: Anda belum melakukan absen masuk hari ini.")
        
        return redirect('index')
    
    # Mengambil data absensi hari ini untuk ditampilkan di template
    absen = None
    if employee:
        absen = Attendance.objects.filter(employee=employee, date=today).first()
    
    # Render halaman dashboard
    return render(request, 'hrd_app/index.html', {
        'employee': employee,
        'absen': absen,
        'today': today
    })

@staff_member_required
def rekap_absensi(request):
    """
    Halaman khusus admin (staff) untuk melihat daftar absensi hari ini.
    """
    today = timezone.now().date()
    # Menampilkan data absensi terbaru di posisi teratas
    laporan = Attendance.objects.filter(date=today).select_related('employee', 'employee__department').order_by('-check_in')
    
    return render(request, 'hrd_app/rekap.html', {
        'laporan': laporan,
        'today': today
    })