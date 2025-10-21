from django.core.mail import send_mail
from django.conf import settings
from typing import Iterable
from customers.models import Customer


def notify_top_customers(customers: Iterable[Customer]) -> int:
    count = 0
    subject = "Congratulations! You're in our Top 1000 customers"
    for cust in customers:
        if not cust.email:
            continue
        message = (
            f"Dear {cust.first_name},\n\n"
            "You've been selected among our top customers this period and are eligible for exclusive rewards. "
            "Open the app or dial *123# to claim your personalized offers!\n\n"
            "Thank you for being with Teleco."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [cust.email], fail_silently=True)
        count += 1
    return count
