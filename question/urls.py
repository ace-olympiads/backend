from django.urls import path
from .views import AddRecentlyVisitedQuestionView, QuestionListCreateView, QuestionRetrieveUpdateDestroyView, RecentlyVisitedQuestionsView

urlpatterns = [
    path('add/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:question_id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
    path('add_recently_visited_question/', AddRecentlyVisitedQuestionView.as_view(), name='add_recently_visited_question'),
    path('recently_visited_questions/', RecentlyVisitedQuestionsView.as_view(), name='recently_visited_questions'),
]
