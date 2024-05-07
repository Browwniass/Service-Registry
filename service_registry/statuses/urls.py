from django.urls import path
from rest_framework import routers
from django.urls import include
from statuses.views.status import StatusChoicesModelView


router = routers.SimpleRouter()
router.register(r'statuses', StatusChoicesModelView)

urlpatterns = [
    path("", include(router.urls)),
]