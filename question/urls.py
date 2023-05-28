from django.urls import path
from .views import QuestionListCreateView, QuestionRetrieveUpdateDestroyView

urlpatterns = [
    path('', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:question_id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
]
