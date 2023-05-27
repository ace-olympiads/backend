from django.urls import path

from .views import AddQuestionView, QuestionDetailView, QuestionListAPIView

urlpatterns = [
    path('add/', AddQuestionView.as_view(), name='add_question'),
    path('<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/', QuestionListAPIView.as_view(), name='question_list'),
]
