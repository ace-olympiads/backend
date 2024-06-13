from django.db import models
from concept.models import Concept
from users.models import Account

    
class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Examination(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Question(models.Model):
    CATEGORY_CHOICES = (
        ('P', 'Premium User'),
        ('G', 'General User'),
    )
    CATEGORY_TAGS = [
        ('Maths', 'Maths'),
        ('Physics', 'Physics'),
        ('Chemistry', 'Chemistry'),
    ]
    question_text = models.CharField(max_length=200)
    question_text_latex = models.TextField(null=True, blank=True)
    video_solution_url = models.URLField(null=True, blank=True)
    text_solution = models.TextField(null=True, blank=True)
    text_solution_latex = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='G')
    category_tag = models.CharField(max_length=20, choices=CATEGORY_TAGS, blank=True,null=True)
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    iframeText = models.TextField(null=True, blank=True)
    examinations = models.ManyToManyField(Examination)

    def __str__(self):
        return self.question_text
    

class Comment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name="comments")
    commenter = models.ForeignKey(Account, on_delete=models.CASCADE,related_name="comments")
    email= models.EmailField()
    content= models.TextField()
    published_at= models.DateTimeField(auto_now_add=True)
    status= models.BooleanField(default=True)

    def __str__(self):
        return self.commenter