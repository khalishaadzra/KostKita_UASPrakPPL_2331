from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.landing, name='landing'),
    path('kamar/', views.daftar_kamar, name='daftar_kamar'),
    path('kamar/<int:pk>/', views.detail_kamar, name='detail_kamar'),
    path('ajukan/<int:kamar_id>/', views.ajukan_sewa, name='ajukan_sewa'),
    path('upload-bukti/<int:pengajuan_id>/', views.upload_bukti, name='upload_bukti'),
    path('cek-status/', views.cek_status_form, name='cek_status_form'),
    path('cek-status/<int:pengajuan_id>/', views.cek_status, name='cek_status'),

    # Auth
    path('admin-panel/login/', views.admin_login, name='admin_login'),
    path('admin-panel/logout/', views.admin_logout, name='admin_logout'),

    # Dashboard
    path('admin-panel/dashboard/', views.dashboard, name='dashboard'),

    # Kamar
    path('admin-panel/kamar/', views.kamar_list, name='kamar_list'),
    path('admin-panel/kamar/tambah/', views.kamar_tambah, name='kamar_tambah'),
    path('admin-panel/kamar/edit/<int:pk>/', views.kamar_edit, name='kamar_edit'),
    path('admin-panel/kamar/hapus/<int:pk>/', views.kamar_hapus, name='kamar_hapus'),

    # Pengajuan
    path('admin-panel/pengajuan/', views.pengajuan_list, name='pengajuan_list'),
    path('admin-panel/pengajuan/<int:pk>/', views.pengajuan_detail, name='pengajuan_detail'),
    path('admin-panel/pengajuan/setujui/<int:pk>/', views.pengajuan_setujui, name='pengajuan_setujui'),
    path('admin-panel/pengajuan/tolak/<int:pk>/', views.pengajuan_tolak, name='pengajuan_tolak'),
    path('admin-panel/pengajuan/selesai/<int:pk>/', views.pengajuan_selesai, name='pengajuan_selesai'),

    # Bukti Bayar
    path('admin-panel/bukti/', views.bukti_list, name='bukti_list'),
    path('admin-panel/bukti/verifikasi/<int:pk>/', views.bukti_verifikasi, name='bukti_verifikasi'),
    path('admin-panel/bukti/tolak/<int:pk>/', views.bukti_tolak, name='bukti_tolak'),

    # Penyewa
    path('admin-panel/penyewa/', views.penyewa_list, name='penyewa_list'),
]