from django.contrib import admin
from .models import Examination, Question, Comment, Tag

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'simulation_link', 'created_at', 'updated_at')
    fields = ('question_text', 'question_text_latex', 'video_solution_url', 'simulation_link', 'text_solution', 'text_solution_latex', 'category', 'concept', 'author', 'tags', 'examinations')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Examination)