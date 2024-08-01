"""Testing that the Investor Withdrawal Viewset is Performing as Expected"""
from unittest.mock import patch, Mock

from django.test import TestCase, RequestFactory

from rest_framework import status
from rest_framework.response import Response

from financing.models.investor import Investor
from financing.models.transaction import Transaction
from financing.services.investor_withdrawal import WithdrawalService
from financing.views.investor_withdrawal_viewset import InvestorWithdrawalViewSet

class TestInvestorWithdrawalViewSet(TestCase):
    """Testing that the Investor Withdrawal Viewset is Performing as Expected"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = InvestorWithdrawalViewSet.as_view({'post': 'create'})
        self.investor = Mock(spec=Investor)
        self.investor.email = 'wertzhayden3@gmail.com'
        self.investor.balance = 1000

    def test_create_invalid_amount(self):
        """Testing that the Correct Error is being thrown when an incorrect amount is attempting to be added"""
        request_data = {"amount": -100, "email": self.investor.email}
        request = self.factory.post('v1/financing/withdrawal/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Invalid amount."})

    @patch('django.shortcuts.get_object_or_404')
    def test_create_investor_not_found(self, mock_get_object_or_404):
        """Testing when the Investor is not Found"""
        mock_get_object_or_404.side_effect = Mock(side_effect=Investor.DoesNotExist)
        request_data = {"amount": 100, "email": "nonexistent@example.com"}
        request = self.factory.post("v1/financing/withdrawal/", request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('django.shortcuts.get_object_or_404')
    def test_create_successful_withdrawal(self, mock_get_object_or_404):
        """Testing that the Withdrawal of the Investors' Balance is Performing as Expected"""
        self.investor.balance = 50
        mock_get_object_or_404.return_value = self.investor
        request_data = {"amount": 100, "email": self.investor.email}
        request = self.factory.post('v1/financing/withdrawal/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data)
