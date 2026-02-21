from django import template
from hrd_app.models import Employee, Department, Attendance
from django.utils import timezone
import datetime

register = template.Library()

@register.simple_tag
def get_admin_stats():
    today = timezone.now().date()
    late_time = datetime.time(8, 30, 0) # Definisi terlambat jika lewat jam 8:30
    
    stats = {
        'total_employees': Employee.objects.count(),
        'present_today': Attendance.objects.filter(date=today, status='Hadir').count(),
        'late_today': Attendance.objects.filter(date=today, check_in__gt=late_time).count(),
        'total_departments': Department.objects.count(),
        'izin_today': Attendance.objects.filter(date=today, status='Izin').count(),
    }
    return stats
