from django.shortcuts import render, redirect
from .models import Employee, Attendance
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages 

def index(request):
    employees = Employee.objects.all()
    today = timezone.now().date()
    
    if request.method == "POST":
        emp_id = request.POST.get('employee_id')
        aksi = request.POST.get('aksi')
        
        try:
            employee = Employee.objects.get(id=emp_id)
        except Employee.DoesNotExist:
            messages.error(request, "Karyawan tidak ditemukan.")
            return redirect('index')
            
        if aksi == "masuk":
            obj, created = Attendance.objects.get_or_create(
                employee=employee, 
                date=today, 
                defaults={'check_in': timezone.now().time()}
            )
            if created:
                messages.success(request, f"Berhasil! Selamat bekerja, {employee.name}.")
            else:
                messages.warning(request, f"Anda sudah absen masuk hari ini.")
                
        elif aksi == "pulang":
            absen = Attendance.objects.filter(employee=employee, date=today).first()
            if absen:
                if not absen.check_out:
                    absen.check_out = timezone.now().time()
                    absen.save()
                    messages.info(request, f"Berhasil! Hati-hati di jalan, {employee.name}.")
                else:
                    messages.warning(request, f"Anda sudah absen pulang hari ini.")
            else:
                messages.error(request, f"Anda belum absen masuk hari ini.")
        
        return redirect('index')

    return render(request, 'hrd_app/index.html', {'employees': employees})

@staff_member_required
def rekap_absensi(request):
    today = timezone.now().date()
    laporan = Attendance.objects.filter(date=today).order_by('-check_in')
    
    return render(request, 'hrd_app/rekap.html', {
        'laporan': laporan,
        'today': today
    })