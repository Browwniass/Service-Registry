from django.urls import path
from .views.project import ProjectModelView

urlpatterns = [
    path("", ProjectModelView.as_view({'get': 'list'}), name="login"),
]