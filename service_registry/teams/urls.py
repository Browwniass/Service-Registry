from django.urls import path
from teams.views.user import UserLoginView, UserLogoutView, UserRegistrationView


urlpatterns = [
    path('auth/registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
]