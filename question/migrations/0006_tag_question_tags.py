# Generated by Django 4.2 on 2023-06-18 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0005_alter_comment_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='question.tag'),
        ),
    ]
