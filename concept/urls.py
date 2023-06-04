from django.urls import path
from .views import (
    AddRecentlyVisitedVideosView,
    ConceptListCreateView,
    ConceptRetrieveUpdateDestroyView,
    RecentlyVisitedVideosView,
    VideoListCreateView,
    VideoRetrieveUpdateDestroyView,
)

urlpatterns = [
    path('', ConceptListCreateView.as_view(), name='concept-list-create'),
    path('<int:concept_id>/', ConceptRetrieveUpdateDestroyView.as_view(), name='concept-retrieve-update-destroy'),
    path('<int:concept_id>/videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('<int:concept_id>/videos/<int:video_id>/', VideoRetrieveUpdateDestroyView.as_view(), name='video-retrieve-update-destroy'),
    path('add_recently_visited_concept_videos/', AddRecentlyVisitedVideosView.as_view(), name='add_recently_visited_concept_videos'),
    path('recently_visited_concept_videos/', RecentlyVisitedVideosView.as_view(), name='recently_visited_concept_videos'),
]
