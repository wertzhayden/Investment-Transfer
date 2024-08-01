"""Service to Process the Withdrawal and Transaction of the Investor"""
from django.db import transaction

from rest_framework.response import Response
from rest_framework import status

from financing.serializers.transaction_serializer import TransactionSerializer
from financing.models.investor import Investor
from financing.constants import WITHDRAWAL, TRANSACTION_PENDING


class WithdrawalService:
    """Service to Process the Withdrawal and Transaction of the Investor"""

    def __init__(self, investor, amount):
        self.investor = investor
        self.amount = int(amount)

    def process_withdrawal(self):
        """Ensure Successful DB Update and Pending Transaction for the given Fund"""
        with transaction.atomic():
            transaction_serializer = self.create_transaction()
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                updated_balance = self.investor.balance - self.amount
                return self.successful_withdrawal_response(transaction_serializer.data, updated_balance)
            else:
                return self.transaction_error_response(transaction_serializer.errors)
        return Response(transaction_serializer.data)

    def create_transaction(self):
        """Creating the Investors' Pending Transaction"""
        transaction_data = {
            "investor": self.investor.id,
            "amount": self.amount,
            "status": TRANSACTION_PENDING,
            "transaction_type": WITHDRAWAL
        }
        return TransactionSerializer(data=transaction_data)

    def successful_withdrawal_response(self, transaction_data, updated_balance):
        """Returning the Successful Transaction and Updated Balance for the Investor"""
        return Response({
            "transaction": transaction_data,
            "updated_balance": updated_balance
        }, status=status.HTTP_201_CREATED)

    def transaction_error_response(self, errors):
        """Returning the Errors associated with a Transaction"""
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)
