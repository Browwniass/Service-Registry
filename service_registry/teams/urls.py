from django.urls import path
from django.urls import include
from rest_framework import routers
from teams.views.user import UserLoginView, UserModelView, UserLogoutView, UserRegistrationView, UserChoiceModelView, BlacklistTokenView, userRoles
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#roots for viewer and admin 
router_admin = routers.SimpleRouter()
router_admin.register(r'users', UserModelView)

urlpatterns = [
    path("adminn/", include(router_admin.urls)),

    path('auth/registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    #path('auth/logout/', UserLogoutView.as_view(), name='user-logout'),
    path('choices/users/', UserChoiceModelView.as_view({'get': 'list'})),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', BlacklistTokenView.as_view(), name='blacklist'),
    path('user_roles/', userRoles, name='userRoles'),
]