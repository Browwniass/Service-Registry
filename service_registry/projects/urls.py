from django.urls import path
from .views.project import ProjectModelView
from rest_framework import routers
from django.urls import include


router = routers.SimpleRouter()
router.register(r'', ProjectModelView)

urlpatterns = [
    path("", include(router.urls))
]