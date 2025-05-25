from django.urls import path
from .views import CustomUserCreate, CustomAccountCreate, ExamCardListCreate, NavbarConfigView, QuestionCardListCreate, VideoCardList
from .firebase_views import (
    FirebaseTokenAuthView, 
    GoogleAuthView, 
    EmailPasswordLoginView, 
    EmailPasswordRegisterView, 
    UserProfileView,
    UserRoleUpdateView
)

app_name = 'users_api'  # Changed to avoid namespace conflict

# URL patterns for API endpoints
api_patterns = [
    # Firebase authentication endpoints
    path('auth/firebase/', FirebaseTokenAuthView.as_view(), name='firebase_auth'),
    path('auth/google/', GoogleAuthView.as_view(), name='google_auth'),
    path('auth/login/', EmailPasswordLoginView.as_view(), name='email_password_login'),
    path('auth/register/', EmailPasswordRegisterView.as_view(), name='email_password_register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/<int:user_id>/', UserProfileView.as_view(), name='user_profile_detail'),
    path('role/<int:user_id>/', UserRoleUpdateView.as_view(), name='user_role_update'),
]

# Legacy URL patterns (for backward compatibility)
legacy_patterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', CustomAccountCreate.as_view(), name="create_account"),
    path('navbar-config/', NavbarConfigView.as_view(), name='navbar_config'),
    path('video-cards/', VideoCardList.as_view(), name='video-cards'),
    path('exam-cards/', ExamCardListCreate.as_view(), name='exam-cards'),
    path('question-cards/', QuestionCardListCreate.as_view(), name='question-cards'),
]

# Combine all URL patterns
urlpatterns = api_patterns + legacy_patterns