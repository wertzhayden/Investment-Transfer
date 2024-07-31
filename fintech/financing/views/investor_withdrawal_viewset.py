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
from financing.constants import WITHDRAWAL, TRANSACTION_PENDING

class InvestorWithdrawalViewSet(ViewSet):

    # @TODO Adding Permissions to allow us to dynamically pull the investors' email

    def create(self, request):
        """"""
        return Response(self.request.user)
        amount = request.data.get("amount", 0)
        investor = Investor.objects.filter(email="wertzhayden2@gmail.com").first()
        if amount and self.does_investor_have_available_funds(investor_balance=investor.balance, amount=amount):
            with transaction.atomic():
                investor.balance -= amount
                investor.save()
                # @ TODO Run Task to Create Transaction Record with "Pending" status
                investor_transaction_data = {
                    "investor": investor.id,
                    "amount": amount,
                    "status": TRANSACTION_PENDING,
                    "transaction_type": WITHDRAWAL
                }
                transaction_serializer = TransactionSerializer(data=investor_transaction_data)
                transaction_serializer.is_valid()
                transaction_serializer.save()                 
                return Response([transaction_serializer.data, investor.balance])

    @staticmethod
    def does_investor_have_available_funds(investor_balance: float, amount: float) -> bool:
        """Validation of Investors' Account"""
        return investor_balance >= amount
