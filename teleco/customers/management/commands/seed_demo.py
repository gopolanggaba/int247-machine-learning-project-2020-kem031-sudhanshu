import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from customers.models import Customer
from products.models import Product, Offer
from billing.models import Recharge
from subscriptions.models import Subscription
from cdr.models import CallDetailRecord


class Command(BaseCommand):
    help = "Seed demo data for Teleco"

    def add_arguments(self, parser):
        parser.add_argument('--customers', type=int, default=2000)

    def handle(self, *args, **options):
        fake = Faker()
        num_customers = options['customers']

        # Products
        products = []
        categories = ['DATA', 'VOICE', 'SMS', 'BUNDLE']
        for i in range(1, 8):
            p, _ = Product.objects.get_or_create(
                code=f"P{i}",
                defaults={
                    'name': f"Product {i}",
                    'category': random.choice(categories),
                    'price': random.randint(2, 30),
                    'description': 'Auto generated product',
                }
            )
            products.append(p)
        # Offers
        for p in products:
            for d in (10, 20, 30):
                Offer.objects.get_or_create(
                    product=p,
                    name=f"{p.name} {d}% Off",
                    defaults={'details': 'Auto offer', 'discount_percent': d, 'is_personalized': d>=20}
                )

        # Customers
        customers = []
        for _ in range(num_customers):
            cust, _ = Customer.objects.get_or_create(
                msisdn=fake.msisdn(),
                defaults={
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.email(),
                    'age': random.randint(18, 70),
                    'gender': random.choice(['M','F','O']),
                }
            )
            customers.append(cust)

        now = timezone.now()
        # Recharges, Subscriptions, and CDRs
        for cust in customers:
            # Recharges
            for _ in range(random.randint(2, 10)):
                Recharge.objects.create(
                    customer=cust,
                    amount=random.randint(1, 50),
                    channel=random.choice(['app', 'ussd', 'web', 'retail']),
                    created_at=now - timezone.timedelta(days=random.randint(0, 60))
                )
            # Subscriptions
            for _ in range(random.randint(1, 5)):
                p = random.choice(products)
                Subscription.objects.create(
                    customer=cust,
                    product=p,
                    offer=random.choice(list(p.offers.all())) if p.offers.exists() else None,
                    started_at=now - timezone.timedelta(days=random.randint(0, 60)),
                    expires_at=now + timezone.timedelta(days=random.randint(1, 30)),
                    is_active=True,
                )
            # CDRs
            for _ in range(random.randint(20, 200)):
                CallDetailRecord.objects.create(
                    customer=cust,
                    call_type=random.choice(['VOICE_OUT','VOICE_IN','SMS_OUT','SMS_IN','DATA']),
                    started_at=now - timezone.timedelta(days=random.randint(0, 30), hours=random.randint(0,23)),
                    duration_seconds=random.randint(0, 600),
                    cost_amount=random.random()
                )
        self.stdout.write(self.style.SUCCESS("Demo data seeded."))
