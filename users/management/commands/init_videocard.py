from django.core.management.base import BaseCommand
from users.models import VideoCard  # adjust to your app name

class Command(BaseCommand):
    help = 'Initialize video cards for ChipTabs component'

    def handle(self, *args, **options):
        # Define initial video card data
        initial_cards = {
            'Newest': [
                {
                    'title': 'Area Under Curve',
                    'subtitle': '3 Videos',
                    'video_url': 'https://www.youtube.com/embed/xec6HTcn2M8',
                },
                {
                    'title': 'Definite Integral',
                    'subtitle': '2 Videos',
                    'video_url': 'https://www.youtube.com/embed/abcdefg1234',
                },
            ],
            'Popular': [
                {
                    'title': 'Probability and Statistics',
                    'subtitle': '5 Videos',
                    'video_url': 'https://www.youtube.com/embed/hijklmn5678',
                },
                {
                    'title': 'Vector and 3D Geometry',
                    'subtitle': '4 Videos',
                    'video_url': 'https://www.youtube.com/embed/opqrstu9012',
                },
            ],
            'Active': [
                {
                    'title': 'Set and Relations',
                    'subtitle': '6 Videos',
                    'video_url': 'https://www.youtube.com/embed/vwxyz3456',
                },
                {
                    'title': 'Indefinite Integral',
                    'subtitle': '1 Video',
                    'video_url': 'https://www.youtube.com/embed/12345abcde',
                },
            ],
        }

        # Clear existing VideoCard entries
        VideoCard.objects.all().delete()

        # Create new VideoCard entries
        for category, cards in initial_cards.items():
            for idx, card_data in enumerate(cards, start=1):
                VideoCard.objects.create(
                    tab=category,  # Use 'tab' instead of 'category'
                    title=card_data['title'],
                    subtitle=card_data['subtitle'],
                    video_url=card_data['video_url'],
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created [{category}] card: {card_data['title']}"
                    )
                )

        self.stdout.write(self.style.SUCCESS('Successfully initialized all video cards.'))
