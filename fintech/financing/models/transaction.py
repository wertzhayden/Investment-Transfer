"""Model to Represent the Features associated with a Transaction between an Investor and a given Fund"""

from django.db import models
from uuid import uuid4

from financing.models.fund import Fund
from financing.models.investor import Investor
from financing.models.base import BaseModel

from financing.constants import TRANSACTION_TYPES, STATUS_CHOICES


class Transaction(BaseModel):
    """Model to Represent the Features associated with a Transaction between an Investor and a given Fund"""
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.FloatField()
    status = models.CharField(max_length=24, choices=STATUS_CHOICES)
    transaction_type = models.CharField(max_length=24, choices=TRANSACTION_TYPES)
