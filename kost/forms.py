from django import forms
from .models import Pengajuan, BuktiBayar, Kamar

class KamarForm(forms.ModelForm):
    class Meta:
        model = Kamar
        fields = ['nomor', 'lantai', 'foto', 'status']
        widgets = {
            'nomor': forms.TextInput(attrs={'class': 'form-control'}),
            'lantai': forms.NumberInput(attrs={'class': 'form-control'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class PengajuanForm(forms.ModelForm):
    class Meta:
        model = Pengajuan
        fields = ['nama', 'umur', 'jenis_kelamin', 'no_hp', 'scan_ktp', 'durasi']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama lengkap sesuai KTP'}),
            'umur': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Umur'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-select'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '08xxxxxxxxxx'}),
            'scan_ktp': forms.FileInput(attrs={'class': 'form-control'}),
            'durasi': forms.Select(attrs={'class': 'form-select', 'id': 'id_durasi'}),
        }

class BuktiBayarForm(forms.ModelForm):
    class Meta:
        model = BuktiBayar
        fields = ['foto_bukti', 'catatan']
        widgets = {
            'foto_bukti': forms.FileInput(attrs={'class': 'form-control'}),
            'catatan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Catatan tambahan (opsional)'}),
        }