# Generated by Django 4.2 on 2023-06-18 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('concept', '0003_alter_video_author'),
        ('question', '0005_alter_comment_options'),
        ('users', '0002_alter_account_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='last_viewed_concept_videos',
            field=models.ManyToManyField(blank=True, to='concept.video'),
        ),
        migrations.AddField(
            model_name='account',
            name='last_viewed_questions',
            field=models.ManyToManyField(blank=True, to='question.question'),
        ),
    ]