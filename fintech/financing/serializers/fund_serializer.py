"""Serializer for the Fund Model"""
from rest_framework import serializers
from financing.models.fund import Fund

class FundSerializer(serializers.ModelSerializer):
    """Serializer for the Fund Model"""

    class Meta:
        model = Fund
        fields = '__all__'
