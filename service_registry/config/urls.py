"""
URL configuration for service_registry project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from project_catalog.views import *
from rest_framework import routers


"""router = routers.SimpleRouter()
router.register(r'project-list', ProjectAPI)
router.register(r'layers', LayerAPI)
router.register(r'users', UserAPI)
router.register(r'observers', ObserverAPI)
router.register(r'history', HistoryOfChangeAPI)
router.register(r'employees', TeamMemberAPIList)"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("projects.urls")),
    path("", include("teams.urls")),

]

""" path("api/", include(router.urls)),   
    path('api/auth/registration/', UserRegistrationView.as_view(), name='user-registration'),
    path('api/auth/login/', UserLoginView.as_view(), name='user-login'),
    path('api/auth/logout/', UserLogoutView.as_view(), name='user-logout'),"""