"""Routing URLs for Financing Viewsets"""

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from financing.views.investor_withdrawal_viewset import InvestorWithdrawalViewSet
from financing.views.transfer_to_fund_viewset import TransferToFundViewSet

financing_router = SimpleRouter()
financing_router.register("withdrawal", InvestorWithdrawalViewSet, basename="withdrawal")
financing_router.register("transfer", TransferToFundViewSet, basename="transfer")
