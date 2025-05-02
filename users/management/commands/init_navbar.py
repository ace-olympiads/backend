from django.core.management.base import BaseCommand
from users.models import NavbarButton  # Replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Initialize navbar configuration'

    def handle(self, *args, **options):
        # Define initial navbar structure
        nav_structure = [
            # About button
            {
                'name': 'about',
                'display_name': 'About',
                'order': 1,
                'parent': None
            },
            # Ace-JEE parent
            {
                'name': 'ace_jee',
                'display_name': 'Ace-JEE',
                'order': 2,
                'parent': None,
                'children': [
                    {
                        'name': 'jee_mains',
                        'display_name': 'JEE Mains',
                        'order': 1
                    },
                    {
                        'name': 'jee_advanced',
                        'display_name': 'JEE Advanced',
                        'order': 2
                    }
                ]
            },
            # Ace-NEET button
            {
                'name': 'ace_neet',
                'display_name': 'Ace-NEET',
                'order': 3,
                'parent': None
            }
        ]
        
        # Clear existing buttons
        NavbarButton.objects.all().delete()
        
        # Create top-level buttons first
        button_objects = {}
        for item in nav_structure:
            button = NavbarButton.objects.create(
                name=item['name'],
                display_name=item['display_name'],
                order=item['order'],
                is_enabled=True
            )
            button_objects[item['name']] = button
            
            # Create children if any
            if 'children' in item:
                for i, child in enumerate(item['children']):
                    NavbarButton.objects.create(
                        name=child['name'],
                        display_name=child['display_name'],
                        order=child['order'],
                        parent=button,
                        is_enabled=True
                    )
        
        self.stdout.write(self.style.SUCCESS('Successfully initialized navbar buttons'))