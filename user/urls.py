from django.urls import path

from .views import AddQuestionView, QuestionDetailView, QuestionListAPIView, SignupView, LoginView, RefreshView

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', RefreshView.as_view()),
    path('question/add/', AddQuestionView.as_view(), name='add_question'),
    path('question/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('questions/', QuestionListAPIView.as_view(), name='question_list'),
]
