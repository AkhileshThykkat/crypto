from rest_framework import serializers
from .models import Organisation, CryptoPrice

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

class CryptoPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoPrice
        fields = '__all__'
