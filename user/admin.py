from django.contrib import admin
from .models import Question

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at', 'updated_at')

admin.site.register(Question, QuestionAdmin)
