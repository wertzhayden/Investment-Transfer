"""Model to Represent the Features associated with a Fund"""

from django.db import models
from uuid import uuid4

from financing.models.base import BaseModel

class Fund(BaseModel):
    """Model to Represent the Features associated with a Fund"""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.TextField()
    minimum_investment = models.IntegerField()
    seat_availability = models.IntegerField()
    total_seats = models.IntegerField()
    current_balance = models.FloatField(default=0, null=True, blank=True)
    max_fund_size = models.IntegerField(null=True, blank=True)