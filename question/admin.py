from django.contrib import admin
from .models import Question,Comment

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at', 'updated_at')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
