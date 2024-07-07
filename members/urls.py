
from django.urls import path
from .views import SignUpView, LoginView, UserDetailView

urlpatterns = [
    path('auth/register/', SignUpView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('api/users/<str:id>/', UserDetailView.as_view(), name='user_detail'),
]