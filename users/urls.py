from django.urls import path
from .views import CustomUserCreate,CustomAccountCreate

app_name = 'users'

urlpatterns = [
    path('create/', CustomUserCreate.as_view(), name="create_user"),
    path('account/', CustomAccountCreate.as_view(),name="create_account")
]
