"""Testing that the Transfer to Fund Viewset is Performing as Expected"""
from unittest.mock import patch, Mock

from django.test import TestCase, RequestFactory

from rest_framework import status
from rest_framework.response import Response

from financing.models.fund import Fund
from financing.models.transaction import Transaction
from financing.services.transfer_to_fund import FundService
from financing.views.transfer_to_fund_viewset import TransferToFundViewSet

class TestTransferToFundViewSet(TestCase):
    """Testing that the Transfer to Fund Viewset is Performing as Expected"""

    def setUp(self):
        self.factory = RequestFactory()
        self.view = TransferToFundViewSet.as_view({'post': 'create'})
        self.transaction = Mock(spec=Transaction)
        self.transaction.id = 1
        self.fund = Mock(spec=Fund)
        self.fund.name = 'Sample Fund'

    @patch('financing.models.transaction.Transaction.objects.filter')
    @patch('financing.models.fund.Fund.objects.filter')
    @patch('financing.services.transfer_to_fund.FundService.is_fund_capacity_exceeded', return_value=True)
    def test_create_fund_capacity_exceeded(self, mock_is_fund_capacity_exceeded, mock_fund_filter, mock_transaction_filter):
        """Testing that the Correct Error is thrown when the Fund Capacity is Exceeded"""
        mock_transaction_filter.return_value.first.return_value = self.transaction
        mock_fund_filter.return_value.first.return_value = self.fund
        request_data = {"transaction_id": self.transaction.id, "fund": self.fund.name}
        request = self.factory.post('v1/financing/transfer/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Fund capacity exceeded"})


    @patch('financing.models.transaction.Transaction.objects.filter')
    @patch('financing.models.fund.Fund.objects.filter')
    @patch('financing.services.transfer_to_fund.FundService.process_fund_transfer')
    @patch('financing.services.transfer_to_fund.FundService.is_fund_capacity_exceeded', return_value=False)
    def test_create_successful_transfer(self, mock_is_fund_capacity_exceeded, mock_process_fund_transfer, mock_fund_filter, mock_transaction_filter):
        """Testing that the Transfer of Funds is Performing Successfully as Expected"""
        mock_transaction_filter.return_value.first.return_value = self.transaction
        mock_fund_filter.return_value.first.return_value = self.fund
        mock_response = Response(status=status.HTTP_201_CREATED)
        mock_process_fund_transfer.return_value = mock_response
        request_data = {"transaction_id": self.transaction.id, "fund": self.fund.name}
        request = self.factory.post('v1/financing/transfer/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_process_fund_transfer.assert_called_once()


    @patch('financing.models.transaction.Transaction.objects.filter')
    @patch('financing.models.fund.Fund.objects.filter')
    def test_create_transaction_or_fund_not_found(self, mock_fund_filter, mock_transaction_filter):
        """Testing that the Transaction is Throwing the Correct Errors when a Transaction or Fund is not Found"""
        mock_transaction_filter.return_value.first.return_value = None
        mock_fund_filter.return_value.first.return_value = None
        request_data = {"transaction_id": self.transaction.id, "fund": self.fund.name}
        request = self.factory.post('v1/financing/transfer/', request_data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Fund capacity exceeded'})
