"""Service for Transferring Money to the Fund of Choice"""
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from financing.serializers.transaction_serializer import TransactionSerializer
from financing.models.fund import Fund
from financing.models.transaction import Transaction
from financing.models.investor import Investor
from financing.constants import TRANSACTION_COMPLETED

class FundService:
    """Service for Transferring Money to the Fund of Choice"""

    def __init__(self, transaction_instance: Transaction, fund: Fund):
        self.transaction_instance = transaction_instance
        self.fund = fund

    def is_fund_capacity_exceeded(self) -> bool:
        """Determine whether the newest Investment Exceeeds the Remaining Amount left in the Fund"""
        if not self.fund or not self.transaction_instance:
            return True
        return self.fund.current_balance + self.transaction_instance.amount > self.fund.max_fund_size and self.fund.seat_availability > 0

    def update_fund_balance_and_seat(self) -> None:
        """Updating the Current Balance and Seat Availability of a given Fund"""
        self.fund.current_balance += self.transaction_instance.amount
        self.fund.seat_availability -= 1
        self.fund.save()

    def update_transaction_status(self) -> None:
        """Updating the Transaction Status to Completed and Reduce the Balance of the Investor"""
        self.transaction_instance.status = TRANSACTION_COMPLETED
        self.transaction_instance.fund = self.fund
        self.transaction_instance.investor.balance -= self.transaction_instance.amount
        self.transaction_instance.investor.save(update_fields=["balance"])
        self.transaction_instance.save()

    def process_fund_transfer(self) -> Response:
        """Ensure that the DB Update is Successful and Return the Latest Transactions' Values"""
        with transaction.atomic():
            self.update_fund_balance_and_seat()
            self.update_transaction_status()
        return Response(TransactionSerializer(self.transaction_instance).data, status=status.HTTP_201_CREATED)
