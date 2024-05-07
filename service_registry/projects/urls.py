from django.urls import path
from .views.project import ProjectModelView
from comments.views import CommentModelView
from teams.views.member import MemberModelView
from projects.views.document import ProjectDocumentModelView
from statuses.views.project_status import ChangeProjectStatusModelView
from statuses.views.layer_status import ChangeLayerStatusModelView
from projects.views.layer import LayerModelView
from teams.views.stackholder import StackholderModelView
from projects.views.stack import StackChoicesModelView
from logs.views import HistoryOfChangeModelView
from rest_framework import routers
from django.urls import include
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register(r'projects', ProjectModelView)
#roots for viewer and member
viewer_project_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
viewer_project_router.register(r'comments', CommentModelView, basename='project-comments')
viewer_project_router.register(r'members', MemberModelView, basename='project-members')
viewer_project_router.register(r'stackholders', StackholderModelView, basename='project-stackholder')
viewer_project_router.register(r'documents', ProjectDocumentModelView, basename='project-documents')
viewer_project_router.register(r'changes', HistoryOfChangeModelView, basename='project-changes')
viewer_project_router.register(r'status_changes', ChangeProjectStatusModelView, basename='project-status-change')
viewer_project_router.register(r'layers', LayerModelView, basename='project-layers')

router.register(r'layers', LayerModelView)
viewer_layer_router = routers.NestedSimpleRouter(router, r'layers', lookup='layer')
viewer_layer_router.register(r'comments', CommentModelView, basename='layer-comments')
viewer_layer_router.register(r'members', MemberModelView, basename='layer-members')
viewer_layer_router.register(r'changes', HistoryOfChangeModelView, basename='layer-changes')
viewer_layer_router.register(r'status_changes', ChangeLayerStatusModelView, basename='layer-status-change')


#roots for viewer and admin 
router_admin = routers.SimpleRouter()
router_admin.register(r'projects', ProjectModelView)
viewer_admin_router = viewer_project_router
router_admin.register(r'layers', LayerModelView)
admin_layer_router = viewer_layer_router

urlpatterns = [
    path("viewer/", include(router.urls)),
    path(r'viewer/', include(viewer_project_router.urls)),
    path(r'viewer/', include(viewer_layer_router.urls)),
    path("member/", include(router.urls)),
    path(r'member/', include(viewer_project_router.urls)),
    path(r'member/', include(viewer_layer_router.urls)),
    path("adminn/", include(router_admin.urls)),
    path(r'adminn/', include(viewer_admin_router.urls)),
    path(r'adminn/', include(admin_layer_router.urls)),
    path('stacks/', StackChoicesModelView.as_view({'get': 'list'}), name='stacks' )
]