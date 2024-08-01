"""Testing each Method within the Withdrawal Service"""
from unittest.mock import patch, Mock

from django.test import TestCase

from rest_framework import status
from rest_framework.response import Response

from financing.constants import WITHDRAWAL, TRANSACTION_PENDING
from financing.models.investor import Investor
from financing.serializers.transaction_serializer import TransactionSerializer
from financing.services.investor_withdrawal import WithdrawalService


class TestWithdrawalService(TestCase):
    """Testing each Method within the Withdrawal Service"""
    def setUp(self):
        self.investor = Mock(spec=Investor)
        self.investor.id = 1
        self.investor.balance = 1000
        self.amount = 100
        self.service = WithdrawalService(self.investor, self.amount)

    @patch('financing.serializers.transaction_serializer.TransactionSerializer.is_valid', return_value=True)
    @patch('financing.serializers.transaction_serializer.TransactionSerializer.save', return_value=None)
    def test_process_withdrawal_success(self, mock_save, mock_is_valid):
        """Testing the Process Withdrawal Method returns the Expected Serialized Values"""
        expected_balance = self.investor.balance - self.amount
        mock_serializer_data = {
            "id": 1,
            "investor": self.investor.id,
            "amount": self.amount,
            "status": TRANSACTION_PENDING,
            "transaction_type": WITHDRAWAL
        }
        with patch.object(self.service, 'create_transaction', return_value=Mock(spec=TransactionSerializer, data=mock_serializer_data)):
            response = self.service.process_withdrawal()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['transaction'], mock_serializer_data)
            self.assertEqual(response.data['updated_balance'], expected_balance)

    @patch('financing.serializers.transaction_serializer.TransactionSerializer.is_valid', return_value=False)
    @patch('financing.serializers.transaction_serializer.TransactionSerializer.errors', return_value={'amount': ['Invalid amount']})
    def test_process_withdrawal(self, mock_errors, mock_is_valid):
        """Testing that the Response and Validation is working as expected"""
        with patch.object(self.service, 'create_transaction', return_value=Mock(spec=TransactionSerializer)):
            response = self.service.process_withdrawal()
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data.get("updated_balance"), 900)

    def test_successful_withdrawal_response(self):
        """Testing the Updated Balance and Status are returing the Expected response"""
        transaction_data = {"id": 1, "amount": self.amount, "status": TRANSACTION_PENDING}
        updated_balance = 900
        response = self.service.successful_withdrawal_response(transaction_data, updated_balance)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            "transaction": transaction_data,
            "updated_balance": updated_balance
        })

    def test_transaction_error_response(self):
        """Testing that we will receive the correct Error Response if thrown"""
        errors = {"amount": ["This field is required."]}
        response = self.service.transaction_error_response(errors)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, errors)
