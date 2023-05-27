from django.db import models

class Concept(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class Video(models.Model):
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    youtube_url = models.URLField()
    thumbnail_url = models.URLField()
    author = models.CharField(max_length=255)
    
    def __str__(self):
        return self.title
