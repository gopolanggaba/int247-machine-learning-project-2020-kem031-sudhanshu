from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

from analyticsapp.models import LeaderboardEntry
from customers.models import Customer
from notifications.services import notify_top_customers


class Command(BaseCommand):
    help = "Send notifications to top 1000 HVC customers from latest leaderboards"

    def handle(self, *args, **options):
        now = timezone.now()
        period_label = "WEEKLY"
        start = now - timedelta(weeks=1)
        end = now

        revenue_lb = LeaderboardEntry.objects.filter(
            kind="REVENUE", period=period_label, period_start=start, period_end=end
        ).order_by('rank')
        customers = Customer.objects.filter(id__in=revenue_lb.values_list('customer_id', flat=True)[:1000])
        sent = notify_top_customers(customers)
        self.stdout.write(self.style.SUCCESS(f"Sent {sent} emails to top customers."))
