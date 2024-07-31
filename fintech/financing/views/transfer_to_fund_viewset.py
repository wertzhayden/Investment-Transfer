""""""
from django.db import transaction
from django.forms.models import model_to_dict

from rest_framework import permissions, status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from financing.models.investor import Investor
from financing.models.fund import Fund
from financing.models.transaction import Transaction
from financing.serializers.investor_serializer import InvestorSerializer
from financing.serializers.transaction_serializer import TransactionSerializer
from financing.constants import WITHDRAWAL, TRANSACTION_COMPLETED

class TransferToFundViewSet(ViewSet):

    # @TODO Adding Permissions to allow us to dynamically pull the investors' email

    def create(self, request):
        """"""
        transaction_id = request.data.get("transaction_id")
        fund_name = request.data.get("fund")
        transaction_instance = Transaction.objects.filter(id=transaction_id).first()
        fund = Fund.objects.filter(name=fund_name).first()

        if transaction_instance and fund and fund.current_balance + transaction_instance.amount > fund.max_fund_size:
            return Response({"error": "Fund capacity exceeded"}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            fund.current_balance += transaction_instance.amount
            fund.seat_availability -= 1
            fund.save()
            transaction_instance.status = TRANSACTION_COMPLETED
            transaction_instance.fund = fund
            transaction_instance.save()
        return Response([TransactionSerializer(transaction_instance).data, fund.seat_availability], status=status.HTTP_201_CREATED)
