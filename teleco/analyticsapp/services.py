from dataclasses import dataclass
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta

from billing.models import Recharge
from cdr.models import CallDetailRecord
from customers.models import Customer


@dataclass
class CustomerUsageSummary:
    customer_id: int
    month_spend: float
    month_calls: int
    month_voice_seconds: int
    month_data_events: int


def summarize_customer_usage(customer: Customer) -> CustomerUsageSummary:
    now = timezone.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    spend = (
        Recharge.objects.filter(customer=customer, created_at__gte=start)
        .aggregate(s=Sum('amount'))['s'] or 0
    )
    cdrs = CallDetailRecord.objects.filter(customer=customer, started_at__gte=start)
    calls = cdrs.count()
    voice_seconds = cdrs.filter(call_type__in=["VOICE_OUT", "VOICE_IN"]).aggregate(s=Sum('duration_seconds'))['s'] or 0
    data_events = cdrs.filter(call_type="DATA").count()
    return CustomerUsageSummary(
        customer_id=customer.id,
        month_spend=float(spend),
        month_calls=calls,
        month_voice_seconds=voice_seconds or 0,
        month_data_events=data_events or 0,
    )
