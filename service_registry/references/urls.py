from django.urls import path
from rest_framework import routers
from django.urls import include
from references.views.complexity import ComplexityChoicesModelView, ComplexityModelView
from references.views.layer_type import LayerTypeChoicesModelView, LayerTypeModelView
from references.views.member_role import MemberRoleChoicesModelView, MemberRoleModelView
from references.views.priority import PriorityChoicesModelView, PriorityModelView
from references.views.project_type import ProjectTypeChoicesModelView, ProjectTypeModelView


router = routers.SimpleRouter()
router.register(r'complexitys', ComplexityChoicesModelView)
router.register(r'layer_types', LayerTypeChoicesModelView)
router.register(r'member_roles', MemberRoleChoicesModelView)
router.register(r'prioritys', PriorityChoicesModelView)
router.register(r'project_types', ProjectTypeChoicesModelView)

admin_references_router = routers.SimpleRouter()
admin_references_router.register(r'complexitys', ComplexityModelView)
admin_references_router.register(r'layer_types', LayerTypeModelView)
admin_references_router.register(r'member_roles', MemberRoleModelView)
admin_references_router.register(r'prioritys', PriorityModelView)
admin_references_router.register(r'project_types', ProjectTypeModelView)

urlpatterns = [
    path("choices/", include(router.urls)),
    path("adminn/references/", include(admin_references_router.urls))
]