from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('imageupload/', include('s3_uploader.urls')),
    path('question/', include('question.urls')),
    path('testimonials/', include('testimonials.urls')),
    path('concepts/', include('concept.urls')),
    
    # API endpoints with prefix - only include users.urls once
    path('api/', include([
        path('users/', include('users.urls')),
    ])),
    
    # Keep the old URL pattern for backward compatibility, but with a different namespace
    path('users/', include(('users.urls', 'legacy_users'), namespace='legacy_users')),
]
