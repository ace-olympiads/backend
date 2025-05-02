from django.contrib import admin
from .models import ExamCard, NewUser, Account, NavbarButton, QuestionCard, VideoCard

admin.site.register(NewUser)
admin.site.register(Account)
admin.site.register(VideoCard)

@admin.register(ExamCard)
class ExamCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'width', 'height')
    search_fields = ('title',)

@admin.register(NavbarButton)
class NavbarButtonAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'is_enabled', 'order')
    list_editable = ('is_enabled', 'order')
    list_filter = ('is_enabled',)
    search_fields = ('name', 'display_name')
    
    
@admin.register(QuestionCard)
class QuestionCardAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_subtext', 'tabs')
    list_filter = ('tabs',)
    search_fields = ('question_text',)