# Generated by Django 4.2 on 2023-06-23 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0006_tag_question_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]