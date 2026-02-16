from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rekap/', views.rekap_absensi, name='rekap'),
]