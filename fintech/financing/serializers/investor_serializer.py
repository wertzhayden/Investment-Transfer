"""Serializer for the Investor Model"""
from rest_framework import serializers
from financing.models.investor import Investor

class InvestorSerializer(serializers.ModelSerializer):
    """Serializer for the Investor Model"""

    class Meta:
        model = Investor
        fields = '__all__'
