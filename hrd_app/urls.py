from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_karyawan, name='login_karyawan'),
    path('', views.index, name='index'),
    path('rekap/', views.rekap_absensi, name='rekap'),
    path('logout/', views.user_logout, name='logout'),
]