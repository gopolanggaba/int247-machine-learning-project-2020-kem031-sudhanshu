from django.core.management.base import BaseCommand
from agents.services import generate_personalized_offers
from agents.models import PersonalizedOffer
from customers.models import Customer


class Command(BaseCommand):
    help = "Generate personalized offers for customers using agentic rules"

    def add_arguments(self, parser):
        parser.add_argument('--limit', type=int, default=1000)

    def handle(self, *args, **options):
        limit = options['limit']
        customers = Customer.objects.all()[:limit]
        created = 0
        for cust in customers:
            suggestions = generate_personalized_offers(cust)
            for s in suggestions:
                PersonalizedOffer.objects.update_or_create(
                    customer=cust,
                    offer=s.offer,
                    defaults={'score': s.score, 'rationale': s.rationale, 'is_active': True}
                )
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Generated/updated {created} personalized offers"))
