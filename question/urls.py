from django.urls import path
from .views import QuestionByTagView, QuestionListCreateView, QuestionRetrieveUpdateDestroyView, CommentsView, SearchAPIView, TagListAPIView

urlpatterns = [
    path('add/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:question_id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
    path('comments/<int:id>/', CommentsView.as_view(), name='comments'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('tag/<int:tag_id>/', QuestionByTagView.as_view(), name='question-by-tag'),
    path('tags/', TagListAPIView.as_view(), name='get-all-tags'),
    path('search/', SearchAPIView.as_view(), name='search'),
]
