# Generated by Django 4.2.5 on 2023-12-14 11:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('concept', '0001_initial'),
        ('question', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('A', 'Admin'), ('M', 'Manager'), ('P', 'Premium User'), ('G', 'General User')], default='G', max_length=1)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='Email Address')),
                ('username', models.CharField(max_length=50, verbose_name='Name')),
                ('contact_no', models.CharField(blank=True, default='', max_length=10, verbose_name='Contact Number')),
                ('image', models.CharField(blank=True, max_length=400, null=True, verbose_name='Image')),
                ('is_superuser', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(blank=True, default='', max_length=30)),
                ('provider', models.CharField(default='CredentialsProvider', max_length=30)),
                ('provider_account_id', models.CharField(blank=True, default='', max_length=30)),
                ('expires_at', models.IntegerField(blank=True, null=True)),
                ('id_token', models.CharField(blank=True, default='', max_length=30)),
                ('session_state', models.CharField(blank=True, default='', max_length=30)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into admin site.', verbose_name='Staff Status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='Active')),
                ('last_viewed_concept_videos', models.ManyToManyField(blank=True, to='concept.video')),
                ('last_viewed_questions', models.ManyToManyField(blank=True, to='question.question')),
            ],
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=150)),
                ('first_name', models.CharField(blank=True, max_length=150)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('about', models.TextField(blank=True, max_length=500, verbose_name='about')),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
