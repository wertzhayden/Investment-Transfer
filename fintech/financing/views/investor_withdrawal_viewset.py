"""Viewset to Withdrawal the Amount inputted from the Investment of a given Investor"""
from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from financing.models.investor import Investor
from financing.models.transaction import Transaction
from financing.serializers.investor_serializer import InvestorSerializer
from financing.serializers.transaction_serializer import TransactionSerializer
from financing.services.investor_withdrawal import WithdrawalService


class InvestorWithdrawalViewSet(ViewSet):
    """Viewset to Withdrawal the Amount inputted from the Investment of a given Investor"""
    def create(self, request):
        """Viewset to Withdrawal the Amount inputted from the Investment of a given Investor"""
        amount = request.data.get("amount", 0)
        email = request.data.get("email")
        if int(amount) <= 0:
            return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)
        investor = get_object_or_404(Investor, email=email)
        if not investor or not investor.balance >= int(amount):
            return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)
        return WithdrawalService(investor, amount).process_withdrawal()
