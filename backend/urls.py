from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('imageupload/', include('s3_uploader.urls')),
    path('question/', include('question.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('users/', include('users.urls')),
    path('concepts/', include('concept.urls')),

]
