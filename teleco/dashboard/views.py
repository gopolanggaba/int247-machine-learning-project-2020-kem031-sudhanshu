from django.shortcuts import render
from django.db.models import Sum, Count
from django.utils import timezone


def home(request):
    from customers.models import Customer
    from billing.models import Recharge
    from cdr.models import CallDetailRecord
    from subscriptions.models import Subscription
    now = timezone.now()

    total_customers = Customer.objects.count()
    total_revenue_month = Recharge.objects.filter(created_at__month=now.month, created_at__year=now.year).aggregate(s=Sum('amount'))['s'] or 0
    active_subscriptions = Subscription.objects.filter(is_active=True).count()
    calls_today = CallDetailRecord.objects.filter(started_at__date=now.date()).count()

    context = {
        'total_customers': total_customers,
        'total_revenue_month': float(total_revenue_month),
        'active_subscriptions': active_subscriptions,
        'calls_today': calls_today,
    }
    return render(request, 'dashboard/home.html', context)

# Create your views here.
