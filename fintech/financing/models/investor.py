"""Model to Represent the Features associated with an Investor"""

from django.db import models
from django.contrib.auth.models import User

from financing.models.base import BaseModel

class Investor(BaseModel):
    """Model to Represent the Features associated with an Investor"""
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True
    )
    balance = models.FloatField(default=0, null=True, blank=True)
