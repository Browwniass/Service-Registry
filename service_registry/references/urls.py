from django.urls import path
from rest_framework import routers
from django.urls import include
from references.views.complexity import ComplexityChoicesModelView
from references.views.layer_type import LayerTypeChoicesModelView
from references.views.member_role import MemberRoleChoicesModelView
from references.views.priority import PriorityChoicesModelView
from references.views.project_type import ProjectTypeChoicesModelView


router = routers.SimpleRouter()
router.register(r'complexitys', ComplexityChoicesModelView)
router.register(r'layer_types', LayerTypeChoicesModelView)
router.register(r'member_roles', MemberRoleChoicesModelView)
router.register(r'prioritys', PriorityChoicesModelView)
router.register(r'project_types', ProjectTypeChoicesModelView)

urlpatterns = [
    path("", include(router.urls)),
]