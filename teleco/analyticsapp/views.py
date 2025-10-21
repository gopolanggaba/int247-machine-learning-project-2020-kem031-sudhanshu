from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
from django.db.models.functions import TruncDate


def revenue_trend_month(request):
    from billing.models import Recharge
    now = timezone.now()
    qs = (
        Recharge.objects
        .filter(created_at__year=now.year, created_at__month=now.month)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .order_by('day')
        .annotate(total=Sum('amount'))
    )
    labels = [str(x['day']) for x in qs]
    values = [float(x['total']) for x in qs]
    return JsonResponse({"labels": labels, "values": values})


def leaderboard(request):
    from analyticsapp.models import LeaderboardEntry
    kind = request.GET.get('kind', 'REVENUE')
    period = request.GET.get('period', 'WEEKLY')
    # Use the latest computed set for the requested period/kind
    latest = (
        LeaderboardEntry.objects.filter(kind=kind, period=period)
        .order_by('-created_at')
        .values('period_start', 'period_end')
        .first()
    )
    if not latest:
        return JsonResponse({"entries": []})
    entries = (
        LeaderboardEntry.objects.filter(
            kind=kind, period=period,
            period_start=latest['period_start'], period_end=latest['period_end']
        )
        .select_related('customer')
        .order_by('rank')
    )
    data = [
        {
            'rank': e.rank,
            'msisdn': e.customer.msisdn,
            'value': float(e.value),
        }
        for e in entries
    ]
    return JsonResponse({"entries": data, "period_start": latest['period_start'], "period_end": latest['period_end']})

# Create your views here.
