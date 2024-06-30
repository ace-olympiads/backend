from django.db import models
from users.models import Account


class Concept(models.Model):
    CATEGORY_CHOICES = [
        ('Maths', 'Maths'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    def __str__(self):
        return self.title


class Video(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=400, blank=True, null= True)
    youtube_url = models.URLField()
    thumbnail_url = models.URLField()
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
