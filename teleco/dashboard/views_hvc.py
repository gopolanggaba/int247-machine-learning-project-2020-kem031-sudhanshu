from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from analyticsapp.models import LeaderboardEntry


def hvc_lists(request):
    now = timezone.now()
    periods = ["HOURLY", "DAILY", "WEEKLY", "MONTHLY", "ANNUAL"]
    kind = request.GET.get('kind', 'REVENUE')
    selected_period = request.GET.get('period', 'WEEKLY')

    if selected_period == 'HOURLY':
        start = now - timedelta(hours=1)
    elif selected_period == 'DAILY':
        start = now - timedelta(days=1)
    elif selected_period == 'WEEKLY':
        start = now - timedelta(weeks=1)
    elif selected_period == 'MONTHLY':
        start = now - timedelta(days=30)
    else:
        start = now - timedelta(days=365)

    entries = LeaderboardEntry.objects.filter(kind=kind, period=selected_period, period_start=start, period_end=now).order_by('rank')

    return render(request, 'dashboard/hvc.html', {
        'periods': periods,
        'kind': kind,
        'selected_period': selected_period,
        'entries': entries,
    })
