from django.urls import path
from .views import CustomUserCreate,CustomAccountCreate, ExamCardListCreate, NavbarConfigView, QuestionCardListCreate, VideoCardList

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', CustomAccountCreate.as_view(),name="create_account"),
    path('navbar-config/', NavbarConfigView.as_view(), name='navbar_config'),
    path('video-cards/', VideoCardList.as_view(), name='video-cards'),
    path('exam-cards/', ExamCardListCreate.as_view(), name='exam-cards'),
    path('question-cards/', QuestionCardListCreate.as_view(), name='question-cards'),
]