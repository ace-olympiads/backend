from django.contrib import admin
from .models import UploadedImage

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('file_name', 's3_url', 'created_at')
    search_fields = ('file_name', 's3_key')
    readonly_fields = ('id', 'created_at')
    list_filter = ('created_at',)