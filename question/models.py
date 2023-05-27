from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    video_solution_url = models.URLField(null=True, blank=True)
    text_solution = models.TextField(null=True, blank=True)
    text_solution_latex = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question_text