from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")

        return self.create_user(email=email, password=password, **extra_fields)


class User(AbstractUser):
    ROLES = (
        ('A', 'Admin'),
        ('M', 'Manager'),
        ('P', 'Premium User'),
        ('G', 'General User'),
    )
    role = models.CharField(max_length=1, choices=ROLES, default='G')
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=50, verbose_name="Name")
    contact_no = models.CharField(max_length=10, verbose_name="Contact Number", default="", blank=True)
    image = models.ImageField(upload_to='users', blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    type=models.CharField(max_length=30,default="",blank=True)
    provider=models.CharField(max_length=30,default='CredentialsProvider')
    provider_account_id=models.CharField(max_length=30,default="",blank=True)
    refresh_token=models.CharField(default="",blank=True,max_length=30)
    access_token=models.CharField(default="",blank=True,max_length=30)
    expires_at=models.IntegerField(null=True,blank=True)
    token_type=models.CharField(default="",blank=True,max_length=30)
    scope=models.CharField(default="",blank=True,max_length=30)
    id_token=models.CharField(default="",blank=True,max_length=30)
    session_state=models.CharField(default="",blank=True,max_length=30)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    is_staff = models.BooleanField(
        verbose_name='Staff Status',
        default=False,
        help_text='Designates whether the user can log into admin site.',
    )

    is_active = models.BooleanField(
        verbose_name='Active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
                  'Unselect this instead of deleting accounts.',
    )
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    

