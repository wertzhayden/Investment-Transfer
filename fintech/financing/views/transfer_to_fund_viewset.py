"""Viewset for Transferring the Investment into the Fund by the Investor"""
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from financing.models.fund import Fund
from financing.models.transaction import Transaction
from financing.services.transfer_to_fund import FundService

class TransferToFundViewSet(ViewSet):
    """Viewset for Transferring the Investment into the Fund by the Investor"""

    def create(self, request):
        """Viewset for Transferring the Investment into the Fund by the Investor"""
        transaction_id = request.data.get("transaction_id")
        fund_name = request.data.get("fund")
        transaction_instance = Transaction.objects.filter(id=transaction_id).first()
        fund = Fund.objects.filter(name=fund_name).first()
        fund_service = FundService(transaction_instance=transaction_instance, fund=fund)
        if fund_service.is_fund_capacity_exceeded():
            return Response({"error": "Fund capacity exceeded"}, status=status.HTTP_400_BAD_REQUEST)
        return fund_service.process_fund_transfer()
