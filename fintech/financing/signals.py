""""""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from financing.models.investor import Investor
from financing.models.fund import Fund

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'financing':
        # Check if data already exists to prevent duplicate entries

        # Create Investor instances if they don't exist
        if Investor.objects.count() == 0:
            for i in range(5):
                Investor.objects.create(
                    email=f"wertzhayden{i}@gmail.com",
                    balance=1000 + i * 100
                )

        # Create Fund instances if they don't exist
        if Fund.objects.count() == 0:
            for i in range(5):
                Fund.objects.create(
                    name=f'Fund {i}', 
                    minimum_investment=5000, 
                    seat_availability=10 + i,
                    total_seats=20, 
                    current_balance=0,
                    max_fund_size=10000000
                )
