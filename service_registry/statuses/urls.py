from django.urls import path
from rest_framework import routers
from django.urls import include
from statuses.views.status import StatusChoicesModelView, StatusModelView


router = routers.SimpleRouter()
router.register(r'statuses', StatusChoicesModelView)

admin_references_router = routers.SimpleRouter()
admin_references_router.register(r'statuses', StatusModelView)

urlpatterns = [
    path("choices/", include(router.urls)),
    path("adminn/references/", include(admin_references_router.urls))
]