from django.core.management.base import BaseCommand
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from analyticsapp.models import LeaderboardEntry
from billing.models import Recharge
from cdr.models import CallDetailRecord
from customers.models import Customer
from django.conf import settings


class Command(BaseCommand):
    help = "Compute top HVC leaderboards (revenue and calls) for multiple periods"

    def handle(self, *args, **options):
        now = timezone.now()
        periods = [
            ("HOURLY", now - timedelta(hours=1), now),
            ("DAILY", now - timedelta(days=1), now),
            ("WEEKLY", now - timedelta(weeks=1), now),
            ("MONTHLY", now - timedelta(days=30), now),
            ("ANNUAL", now - timedelta(days=365), now),
        ]

        for label, start, end in periods:
            self.compute_revenue(label, start, end)
            self.compute_calls(label, start, end)
        self.stdout.write(self.style.SUCCESS("Leaderboards computed."))

    def compute_revenue(self, period_label, start, end):
        limit = getattr(settings, 'HVC_TOP_LIMIT', 1000)
        # Aggregate recharges as revenue proxy
        agg = (
            Recharge.objects.filter(created_at__gte=start, created_at__lt=end)
            .values('customer')
            .annotate(total=Sum('amount'))
            .order_by('-total')[:limit]
        )
        LeaderboardEntry.objects.filter(kind="REVENUE", period=period_label, period_start=start, period_end=end).delete()
        bulk = []
        for rank, row in enumerate(agg, start=1):
            bulk.append(
                LeaderboardEntry(
                    kind="REVENUE",
                    period=period_label,
                    period_start=start,
                    period_end=end,
                    customer_id=row['customer'],
                    value=row['total'],
                    rank=rank,
                )
            )
        LeaderboardEntry.objects.bulk_create(bulk, ignore_conflicts=True)

    def compute_calls(self, period_label, start, end):
        limit = getattr(settings, 'HVC_TOP_LIMIT', 1000)
        agg = (
            CallDetailRecord.objects.filter(started_at__gte=start, started_at__lt=end)
            .values('customer')
            .annotate(total=Count('id'))
            .order_by('-total')[:limit]
        )
        LeaderboardEntry.objects.filter(kind="CALLS", period=period_label, period_start=start, period_end=end).delete()
        bulk = []
        for rank, row in enumerate(agg, start=1):
            bulk.append(
                LeaderboardEntry(
                    kind="CALLS",
                    period=period_label,
                    period_start=start,
                    period_end=end,
                    customer_id=row['customer'],
                    value=row['total'],
                    rank=rank,
                )
            )
        LeaderboardEntry.objects.bulk_create(bulk, ignore_conflicts=True)
