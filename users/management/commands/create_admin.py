from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Account

class Command(BaseCommand):
    help = 'Create an admin user'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Admin username', default='admin')
        parser.add_argument('--email', type=str, help='Admin email', required=True)
        parser.add_argument('--password', type=str, help='Admin password', default='admin123')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if Account.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists')
            )
            return

        # Create admin user
        admin_user = Account.objects.create_user(
            username=username,
            email=email,
            password=password,
            role='A',  # Admin role
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created admin user: {username} ({email})')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Password: {password}')
        )
        self.stdout.write(
            self.style.WARNING('Please change the password after first login!')
        )