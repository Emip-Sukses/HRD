from django.shortcuts import render, redirect
from .models import Employee, Attendance
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 
import math

# Konfigurasi Geolocation Kantor
LOCATIONS = [
    {"name": "Kantor Utama", "lat": -6.9242479, "lon": 107.7147351},
    {"name": "Gudang", "lat": -6.92453208361585, "lon": 107.71120702873829},
]
ALLOWED_RADIUS = 100  # dalam meter

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak antara dua koordinat menggunakan rumus Haversine (meter).
    """
    R = 6371000  # Radius bumi dalam meter
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

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
        
        # Otentikasi user menggunakan backend Django (By User/NIK)
        user = authenticate(request, username=username, password=password)
        
        # Jika gagal, coba cari berdasarkan Nama Karyawan (Case Insensitive)
        if user is None:
            try:
                # Cari karyawan yang namanya mengandung inputan
                emps = Employee.objects.filter(name__iexact=username)
                
                # HANYA jika ditemukan SATU karyawan unik
                if emps.count() == 1:
                    emp = emps.first()
                    if emp and emp.user:
                        user = authenticate(request, username=emp.user.username, password=password)
                elif emps.count() > 1:
                    messages.warning(request, "Ada beberapa karyawan dengan nama tersebut. Silakan login menggunakan NIK/ID Anda.")
                    return render(request, 'hrd_app/login_karyawan.html')
            except Exception:
                pass
        
        if user is not None:
            # Memastikan hanya non-staff (karyawan biasa) yang bisa login di sini
            if not user.is_staff:
                login(request, user)
                if user.check_password('password123'):
                    messages.warning(request, "⚠️ PENTING: Anda masih menggunakan Password Default. Segera hubungi HRD untuk menggantinya demi keamanan.")
                else:
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
        lat = request.POST.get('lat')
        lon = request.POST.get('lon')

        # 1. Validasi Keberadaan Koordinat
        if not lat or not lon:
            messages.error(request, "Gagal mendeteksi lokasi. Pastikan GPS aktif dan izinkan akses lokasi di browser.")
            return redirect('index')

        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            messages.error(request, "Data lokasi tidak valid.")
            return redirect('index')

        # 2. Validasi Jarak ke Kantor/Gudang
        is_in_range = False
        min_distance = float('inf')
        location_name = ""

        for loc in LOCATIONS:
            dist = calculate_distance(lat, lon, loc['lat'], loc['lon'])
            if dist < min_distance:
                min_distance = dist
                location_name = loc['name']
            
            if dist <= ALLOWED_RADIUS:
                is_in_range = True
                break

        if not is_in_range:
            messages.error(request, f"Akses Ditolak: Anda berada di luar area ({int(min_distance)} meter dari titik terdekat).")
            return redirect('index')

        if aksi == "masuk":
            # get_or_create memastikan tidak ada duplikasi data absensi di hari yang sama
            obj, created = Attendance.objects.get_or_create(
                employee=employee,
                date=today,
                defaults={
                    'check_in': timezone.localtime().time(),
                    'lat_in': lat,
                    'lon_in': lon
                }
            )
            if created:
                messages.success(request, f"Absen masuk berhasil pada pukul {obj.check_in.strftime('%H:%M:%S')}. Lokasi terverifikasi!")
            else:
                messages.warning(request, "Anda sudah tercatat melakukan absen masuk hari ini.")
                
        elif aksi == "pulang":
            # Mencari data absensi hari ini yang jam pulangnya masih kosong
            absen = Attendance.objects.filter(employee=employee, date=today).first()
            if absen:
                if not absen.check_out:
                    absen.check_out = timezone.localtime().time()
                    absen.lat_out = lat
                    absen.lon_out = lon
                    absen.save()
                    messages.info(request, f"Absen pulang berhasil pada pukul {absen.check_out.strftime('%H:%M:%S')}. Hati-hati di jalan!")
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

@login_required
def riwayat_saya(request):
    """
    Karyawan bisa melihat histori absensinya sendiri.
    """
    employee = None
    try:
        employee = request.user.employee
    except Employee.DoesNotExist:
        messages.error(request, "Akun Anda tidak terhubung ke data karyawan.")
        return redirect('index')
    
    # Riwayat 30 hari terakhir
    histori = Attendance.objects.filter(employee=employee).order_by('-date')[:30]
    
    return render(request, 'hrd_app/riwayat_saya.html', {'histori': histori})

@login_required
def ganti_password(request):
    """
    Karyawan bisa mengganti password mereka sendiri secara mandiri.
    """
    if request.method == "POST":
        password_lama = request.POST.get('password_lama')
        password_baru = request.POST.get('password_baru')
        konfirmasi_password = request.POST.get('konfirmasi_password')
        
        # 1. Validasi Password Lama
        if not request.user.check_password(password_lama):
            messages.error(request, "Password lama yang Anda masukkan salah!")
            return redirect('ganti_password')
            
        # 2. Validasi Kesamaan Password Baru
        if password_baru != konfirmasi_password:
            messages.error(request, "Konfirmasi password baru tidak cocok!")
            return redirect('ganti_password')
            
        # 3. Validasi Panjang Password
        if len(password_baru) < 8:
            messages.error(request, "Password baru minimal harus 8 karakter!")
            return redirect('ganti_password')
            
        # 4. Simpan Password Baru
        request.user.set_password(password_baru)
        request.user.save()
        
        # Penting: Setelah ganti password, sesi login akan terputus kecuali kita update session hash
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(request, request.user)
        
        messages.success(request, "Password Anda berhasil diperbarui!")
        return redirect('index')
        
    return render(request, 'hrd_app/ganti_password.html')