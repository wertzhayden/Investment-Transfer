"""Base model to Store the Created and Updated Timestamps per Fund, Investor and Transaction"""

from django.db import models
from uuid import uuid4

class BaseModel(models.Model):
    """
    Base model for listing database models.

    Attributes:
        id (UUIDField): Primary key for database record.
        created_at (DateTimeField): Timestamp for when record is created.
        updated_at (DateTimeField): Timestamp for when record was last updated, done automatically.
    """

    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        """BaseModel metadata options."""

        abstract = True