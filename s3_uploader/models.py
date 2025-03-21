from django.db import models
from django.conf import settings
import uuid

class UploadedImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=512)
    s3_url = models.URLField(max_length=1024)
    content_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.file_name