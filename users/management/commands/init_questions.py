from django.core.management.base import BaseCommand
from users.models import QuestionCard

class Command(BaseCommand):
    help = 'Initialize question cards for Bookpage component'

    def handle(self, *args, **options):
        initial_questions = [
            {
                'question_text': 'What is the angular velocity of a uniform rod immediately after an inelastic collision at one end?',
                'question_subtext': 'Assume the rod is initially at rest and pivoted at the center.',
                'image': 'question_images/default.png',
                'tabs': 'JEE-Mains',
            },
            {
                'question_text': 'Determine the angular speed of a rod after being struck perpendicularly at one end by a moving particle.',
                'question_subtext': 'Consider conservation of angular momentum about the center of mass.',
                'image': 'question_images/default.png',
                'tabs': 'JEE-Mains',
            },
            {
                'question_text': 'Find the angular velocity of a uniform rod when a particle collides with it and sticks.',
                'question_subtext': 'The collision occurs at the edge of the rod lying horizontally on a frictionless surface.',
                'image': 'question_images/default.png',
                'tabs': 'JEE-Mains',
            }
            # add more question cards as needed
        ]


        QuestionCard.objects.all().delete()

        for q in initial_questions:
            QuestionCard.objects.create(
                question_text=q['question_text'],
                question_subtext=q['question_subtext'],
                image=q['image'],
                tabs=q['tabs'],
            )
            self.stdout.write(self.style.SUCCESS(f"Created question card: {q['question_text']}"))

        self.stdout.write(self.style.SUCCESS("Successfully initialized all question cards."))