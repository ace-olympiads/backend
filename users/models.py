from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, username, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150)
    first_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    about = models.TextField(_(
        'about'), max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return self.username

class Account(models.Model):
    ROLES = (
        ('A', 'Admin'),
        ('M', 'Manager'),
        ('P', 'Premium User'),
        ('G', 'General User'),
    )
    role = models.CharField(max_length=1, choices=ROLES, default='G')
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=50, verbose_name="Name")
    contact_no = models.CharField(max_length=10, verbose_name="Contact Number", default="", blank=True)
    image = models.CharField(max_length=400, verbose_name="Image",null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True)
    type=models.CharField(max_length=30,default="",blank=True)
    provider=models.CharField(max_length=30,default='CredentialsProvider')
    provider_account_id=models.CharField(max_length=30,default="",blank=True)
    expires_at=models.IntegerField(null=True,blank=True)
    id_token=models.CharField(default="",blank=True,max_length=30)
    session_state=models.CharField(default="",blank=True,max_length=30)
    last_viewed_questions = models.ManyToManyField('question.Question', blank=True)
    last_viewed_concept_videos = models.ManyToManyField('concept.Video', blank=True)
    REQUIRED_FIELDS = ['username','email']
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
    
