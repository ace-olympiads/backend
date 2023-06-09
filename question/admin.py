from django.contrib import admin
from .models import Examination, Question, Comment, Tag

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'created_at', 'updated_at')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Examination)