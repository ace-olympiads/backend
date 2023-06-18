from django.urls import path
from .views import QuestionListCreateView, QuestionRetrieveUpdateDestroyView, CommentsView

urlpatterns = [
    path('add/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:question_id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
    path('comments/<int:id>/', CommentsView.as_view(), name='comments'),
    path('comments/', CommentsView.as_view(), name='comments'),
]
