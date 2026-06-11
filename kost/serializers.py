from rest_framework import serializers
from .models import Kamar, Pengajuan, BuktiBayar

class KamarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kamar
        fields = '__all__'

class PengajuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuan
        fields = '__all__'

class BuktiBayarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuktiBayar
        fields = '__all__'