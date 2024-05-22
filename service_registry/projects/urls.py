from django.urls import path
from projects.views.project import ProjectModelView, ProjectChoiceModelView
from comments.views import CommentModelView
from teams.views.member import MemberModelView
from projects.views.document import ProjectDocumentModelView
from statuses.views.project_status import ChangeProjectStatusModelView
from statuses.views.layer_status import ChangeLayerStatusModelView
from projects.views.layer import LayerModelView
from teams.views.stackholder import StackholderModelView
from projects.views.stack import StackChoicesModelView, StackElementChoicesModelView, StackModelView , StackElementModelView 
from projects.views.quarter import QuarterChoicesModelView, QuarterModelView
from logs.views import NestedHistoryOfChangeModelView, FullHistoryOfChangeModelView
from teams.views.worker import WorkerModelView
from teams.views.viewer import ViewerModelView
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
viewer_project_router.register(r'changes', NestedHistoryOfChangeModelView, basename='project-changes')
viewer_project_router.register(r'status_changes', ChangeProjectStatusModelView, basename='project-status-change')
viewer_project_router.register(r'layers', LayerModelView, basename='project-layers')
viewer_project_router.register(r'viewers', ViewerModelView, basename='project-viewers')

router.register(r'layers', LayerModelView)
viewer_layer_router = routers.NestedSimpleRouter(router, r'layers', lookup='layer')
viewer_layer_router.register(r'comments', CommentModelView, basename='layer-comments')
viewer_layer_router.register(r'members', MemberModelView, basename='layer-members')
viewer_layer_router.register(r'changes', NestedHistoryOfChangeModelView, basename='layer-changes')
viewer_layer_router.register(r'status_changes', ChangeLayerStatusModelView, basename='layer-status-change')


#roots for viewer and admin 
router_admin = routers.SimpleRouter()
router_admin.register(r'projects', ProjectModelView)
router_admin.register(r'layers', LayerModelView)
router_admin.register(r'quarters', QuarterModelView)
router_admin.register(r'changes', FullHistoryOfChangeModelView)
router_admin.register(r'workers', WorkerModelView)
router_admin.register(r'viewers', ViewerModelView)
router_admin.register(r'stacks', StackModelView)
admin_stack_router = routers.NestedSimpleRouter(router_admin, r'stacks', lookup='stack')
admin_stack_router.register(r'stack_elements', StackElementModelView, basename='stack-elements')
router_admin.register(r'stack_elements', StackElementModelView)


urlpatterns = [
    path("viewer/", include(router.urls)),
    path(r'viewer/', include(viewer_project_router.urls)),
    path(r'viewer/', include(viewer_layer_router.urls)),
    path("member/", include(router.urls)),
    path(r'member/', include(viewer_project_router.urls)),
    path(r'member/', include(viewer_layer_router.urls)),
    path("adminn/", include(router_admin.urls)),
    path(r'adminn/', include(viewer_project_router.urls)),
    path(r'adminn/', include(viewer_layer_router.urls)),
    path(r'adminn/', include(admin_stack_router.urls)),
    path('stacks/', StackChoicesModelView.as_view({'get': 'list'})),
    path('choices/quarters/', QuarterChoicesModelView.as_view({'get': 'list'})),
    path('choices/stacks/', StackChoicesModelView.as_view({'get': 'list'})),
    path('choices/stack_elements/', StackElementChoicesModelView.as_view({'get': 'list'})),
    path('choices/projects/', ProjectChoiceModelView.as_view({'get': 'list'}))
]