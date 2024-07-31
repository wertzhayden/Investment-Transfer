"""Model to Represent the Features associated with an Investor"""

from django.db import models
from django.contrib.auth.models import User

from financing.models.base import BaseModel

class Investor(BaseModel):
    """Model to Represent the Features associated with an Investor"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0, null=True, blank=True)
