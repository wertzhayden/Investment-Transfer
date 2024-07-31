""""""
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import User
from financing.models.investor import Investor
from financing.models.fund import Fund

@receiver(post_migrate)
def create_initial_data(sender, **kwargs):
    if sender.name == 'financing':
        # Check if data already exists to prevent duplicate entries
        if User.objects.count() == 0:
            users = []
            for i in range(5):
                user = User.objects.create(
                    email=f"wertzhayden{i}@gmail.com"
                )
                users.append(user)
        else:
            users = list(User.objects.all()[:5])

        if Investor.objects.count() == 0:
            for i, user in enumerate(users):
                Investor.objects.create(
                    user=user,
                    email=f"wertzhayden{i}@gmail.com", 
                    balance=1000 + i * 100
                )

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
