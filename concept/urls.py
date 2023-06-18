from django.urls import path
from .views import (
    ConceptListCreateView,
    ConceptRetrieveUpdateDestroyView,
    VideoListCreateView,
    VideoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', ConceptListCreateView.as_view(), name='concept-list-create'),
    path('<int:concept_id>/', ConceptRetrieveUpdateDestroyView.as_view(), name='concept-retrieve-update-destroy'),
    path('<int:concept_id>/videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('<int:concept_id>/videos/<int:video_id>/', VideoRetrieveUpdateDestroyView.as_view(), name='video-retrieve-update-destroy'),
]
