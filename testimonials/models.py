from django.db import models

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation=models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
