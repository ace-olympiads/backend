from django.urls import path
from .views import ExaminationListAPIView, QuestionByExaminationView, UserCommentsView,QuestionByTagView, QuestionListCreateView, QuestionRetrieveUpdateDestroyView, CommentsView, SearchAPIView, TagListAPIView, ImageUploadView

urlpatterns = [
    path('add/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('<int:question_id>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-retrieve-update-destroy'),
    path('comments/<int:id>/', CommentsView.as_view(), name='comments'),
    path('comments/', CommentsView.as_view(), name='comments'),
    path('user-comments/<str:email>/', UserCommentsView.as_view(), name='user-comments'),
    path('tag/<int:tag_id>/', QuestionByTagView.as_view(), name='question-by-tag'),
    path('tags/', TagListAPIView.as_view(), name='get-all-tags'),
    path('search/', SearchAPIView.as_view(), name='search'),
    path('examination/<int:examination_id>/', QuestionByExaminationView.as_view(), name='question-by-examination'),
    path('examinations/', ExaminationListAPIView.as_view(), name='get-all-examinations'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]
