from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional
from django.db.models import Sum, Count
from django.utils import timezone

from customers.models import Customer
from products.models import Product, Offer
from subscriptions.models import Subscription
from billing.models import Recharge
from cdr.models import CallDetailRecord


@dataclass
class OfferSuggestion:
    offer: Offer
    score: float
    rationale: str


def generate_personalized_offers(customer: Customer, max_offers: int = 3) -> List[OfferSuggestion]:
    now = timezone.now()
    # Simple heuristic + agent-like rules; could be swapped with LLM
    recent_calls = CallDetailRecord.objects.filter(customer=customer, started_at__gte=now - timezone.timedelta(days=30))
    total_calls = recent_calls.count()
    total_voice_seconds = recent_calls.filter(call_type__in=["VOICE_OUT", "VOICE_IN"]).aggregate(s=Sum('duration_seconds'))['s'] or 0
    data_events = recent_calls.filter(call_type="DATA").count()

    recent_spend = Recharge.objects.filter(customer=customer, created_at__gte=now - timezone.timedelta(days=30)).aggregate(s=Sum('amount'))['s'] or 0
    active_products = set(
        Subscription.objects.filter(customer=customer, is_active=True).values_list('product__category', flat=True)
    )

    candidate_offers = Offer.objects.filter(is_active=True).select_related('product')
    scored: List[OfferSuggestion] = []

    for off in candidate_offers:
        score = 0.0
        reasons = []
        if off.product.category == 'VOICE' and total_voice_seconds > 3000:
            score += 0.6
            reasons.append('High voice usage in last 30 days')
        if off.product.category == 'DATA' and data_events > 50:
            score += 0.6
            reasons.append('Frequent data sessions in last 30 days')
        if off.product.category in active_products:
            score += 0.2
            reasons.append('Complementary to active subscriptions')
        if recent_spend and float(recent_spend) > 50:
            score += 0.2
            reasons.append('Recent higher recharge spend')
        if off.discount_percent >= 20:
            score += 0.2
            reasons.append('Attractive discount')

        if score > 0:
            scored.append(OfferSuggestion(offer=off, score=score, rationale='; '.join(reasons)))

    scored.sort(key=lambda x: x.score, reverse=True)
    return scored[:max_offers]
