

from django.core.management.base import BaseCommand
from users.models import ExamCard

class Command(BaseCommand):
    help = 'Initialize exam cards for the Examlist component'

    def handle(self, *args, **options):
        # Define the initial set of exam cards
        initial_cards = [
            {
                'title': 'JEE-Advanced',
                'description': 'Forum is ready by BBPress. Your users can make topics and talk.',
                'icon': '/assets/adv.svg',
                'width': 50,
                'height': 50,
            },
            {
                'title': 'JEE-Mains',
                'description': 'Your users can create groups to let other users to join and talk',
                'icon': '/assets/mains.svg',
                'width': 50,
                'height': 50,
            },
            {
                'title': 'NEET',
                'description': 'Members, Groups list can be modified by drag & drop live builder.',
                'icon': '/assets/neet.svg',
                'width': 50,
                'height': 50,
            },
        ]

        # Wipe out existing data
        ExamCard.objects.all().delete()

        # Create new records
        for card in initial_cards:
            ExamCard.objects.create(
                title=card['title'],
                description=card['description'],
                icon=card['icon'],
                width=card['width'],
                height=card['height'],
            )
            self.stdout.write(self.style.SUCCESS(f"Created exam card: {card['title']}"))

        self.stdout.write(self.style.SUCCESS("Successfully initialized all exam cards."))
