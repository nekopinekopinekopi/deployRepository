from django.urls import path
from .views import (
  WelcomeView, UserRegistView, UserLoginView, UserLogoutView,
  UserDetailView, UserUpdateView
)


app_name = 'accounts'

urlpatterns = [
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('user_regist/', UserRegistView.as_view(), name='user_regist'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('user_detail/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/', UserUpdateView.as_view(), name='user_update'),
]
