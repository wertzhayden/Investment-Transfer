"""Serializer for the Transaction Model"""
from rest_framework import serializers
from financing.models.transaction import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction Model"""

    class Meta:
        model = Transaction
        fields = '__all__'
