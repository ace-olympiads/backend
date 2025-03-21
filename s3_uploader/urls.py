# s3_uploader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('image/', views.get_presigned_url, name='get_presigned_url'),
]