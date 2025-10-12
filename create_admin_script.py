#!/usr/bin/env python
"""
Script to create an admin user
Run this with: python manage.py shell < create_admin_script.py
"""

from users.models import Account

# Admin user details
username = 'admin'
email = 'admin@example.com'  # Change this to your email
password = 'admin123'  # Change this to a secure password

# Check if user already exists
if Account.objects.filter(email=email).exists():
    print(f'User with email {email} already exists')
else:
    # Create admin user
    admin_user = Account.objects.create_user(
        username=username,
        email=email,
        password=password,
        role='A',  # Admin role
        is_staff=True,
        is_superuser=True
    )
    print(f'Successfully created admin user: {username} ({email})')
    print(f'Password: {password}')
    print('Please change the password after first login!')