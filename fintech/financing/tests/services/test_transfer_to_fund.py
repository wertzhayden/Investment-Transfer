"""Testing that the Fund Service is Performing as Expected"""
from unittest.mock import patch, Mock

from django.test import TestCase

from rest_framework import status
from rest_framework.response import Response

from financing.constants import TRANSACTION_COMPLETED
from financing.models.fund import Fund
from financing.models.transaction import Transaction
from financing.models.investor import Investor
from financing.serializers.transaction_serializer import TransactionSerializer
from financing.services.transfer_to_fund import FundService

class TestFundService(TestCase):
    """Testing that the Fund Service is Performing as Expected"""
    def setUp(self):
        self.investor = Mock(spec=Investor)
        self.investor.id = 1
        self.investor.balance = 10000
        
        self.fund = Mock(spec=Fund)
        self.fund.id = 1
        self.fund.current_balance = 50000
        self.fund.max_fund_size = 100000
        self.fund.seat_availability = 5
        
        self.transaction = Mock(spec=Transaction)
        self.transaction.id = 1
        self.transaction.amount = 1000
        self.transaction.investor = self.investor

        self.service = FundService(self.transaction, self.fund)

    def test_is_fund_capacity_exceeded_true(self):
        """Testing that the Method is Correctly identifying when the Max Fund Size is Exceeded"""
        self.fund.current_balance = 99500
        self.fund.max_fund_size = 100000
        self.assertTrue(self.service.is_fund_capacity_exceeded())

    def test_is_fund_capacity_exceeded_false(self):
        """Testing that the Investment fits within the Fund Size"""
        self.fund.current_balance = 50000
        self.fund.max_fund_size = 100000
        self.assertFalse(self.service.is_fund_capacity_exceeded())

    def test_update_fund_balance_and_seat(self):
        """Testing to ensure that the Fund Balance and Seat Availability is Updated as Expected"""
        initial_balance = self.fund.current_balance
        initial_seat_availability = self.fund.seat_availability
        amount = self.transaction.amount
        self.service.update_fund_balance_and_seat()
        self.assertEqual(self.fund.current_balance, initial_balance + amount)
        self.assertEqual(self.fund.seat_availability, initial_seat_availability - 1)
        self.fund.save.assert_called_once()

    def test_update_transaction_status(self):
        """Testing that the Transaction Status is Properly Updated when the Fund Transaction is Completed"""
        initial_balance = self.investor.balance
        amount = self.transaction.amount
        self.service.update_transaction_status()
        self.assertEqual(self.transaction.status, TRANSACTION_COMPLETED)
        self.assertEqual(self.transaction.fund, self.fund)
        self.assertEqual(self.investor.balance, initial_balance - amount)
        self.transaction.save.assert_called_once()
        self.investor.save.assert_called_once_with(update_fields=["balance"])

    @patch.object(FundService, 'update_fund_balance_and_seat')
    @patch.object(FundService, 'update_transaction_status')
    def test_process_fund_transfer(self, mock_update_transaction_status, mock_update_fund_balance_and_seat):
        """Testing to Ensure that the Investment is Properly Transferred to the Fund"""
        serializer_mock = Mock(spec=TransactionSerializer)
        serializer_mock.data = {
            "id": self.transaction.id,
            "amount": self.transaction.amount,
            "status": TRANSACTION_COMPLETED,
        }
        with patch('financing.services.transfer_to_fund.TransactionSerializer', return_value=serializer_mock):
            response = self.service.process_fund_transfer()
            mock_update_fund_balance_and_seat.assert_called_once()
            mock_update_transaction_status.assert_called_once()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, serializer_mock.data)
