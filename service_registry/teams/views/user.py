from teams.models.user import User
from teams.serializers.user import UserSerializer, UserChoiceSerializer, AdminUserSerializer
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from teams.models.viewer import Viewer
from teams.models.worker import Worker
from teams.models.member import Member
from teams.models.stackholder import Stackholder
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets
from rest_framework.decorators import api_view
from config.permissions import AdminOnly, IsRoleOwnRoot


class UserRegistrationView(APIView):
    def post(self, request):
        if request.user.is_authenticated and request.user.is_admin:
            serializer = AdminUserSerializer(data=request.data)
        else:
            serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            new_user = serializer.save()
            new_viewer = Viewer(user=new_user)
            new_viewer.save()

            refresh = RefreshToken.for_user(new_user) # Создание Refesh и Access
            refresh.payload.update({
                'user_id': new_user.id,
                'username': new_user.username
            })
            return Response({'data': serializer.data, 'refresh': str(refresh), 
                'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def userRole(request):
    if request.user.is_authenticated:
        is_admin = request.user.is_admin
        is_worker = Worker.objects.filter(user=request.user).exists()
        #is_member =  (member.first().is_archived == False) and member
        is_viewer = Viewer.objects.filter(user=request.user).exists()
        is_stackholder = Stackholder.objects.filter(viewer__user=request.user).exists()
        data = {
            'admin': {'is_admin': is_admin},
            'is_worker': {'is_worker': is_worker},
            'is_viewer': {'is_viewer': is_viewer, 'is_stackholder': is_stackholder}
        }
        return data
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            #login(request, user)
            refresh = RefreshToken.for_user(user)

            refresh.payload.update({
            'user_id': user.id,
            'username': user.username
            })
            
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})
    

class UserChoiceModelView(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserChoiceSerializer
    pagination_class = None 
    
    def get_queryset(self):
        params = self.request.query_params
        if 'not_viewer' in params:
            user_viewers = Viewer.objects.values_list('user_id', flat=True)
            return User.objects.exclude(id__in=user_viewers)
        return User.objects.all()
    

class BlacklistTokenView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def userRoles(request):
    if request.user.is_authenticated:
        is_admin = request.user.is_admin
        worker = Worker.objects.filter(user=request.user)
        is_viewer = Viewer.objects.filter(user=request.user).exists()
        
        data = {
            'admin': {'is_admin': is_admin},
            'is_worker': {'is_worker': worker.exists()},
            'is_viewer': {'is_viewer': is_viewer}
        }
        if 'project' in request.query_params:
            requested_project = request.query_params['project']
            is_project_stackholder = Stackholder.objects.filter(viewer__user=request.user, project=requested_project).exists()
            is_project_member = Member.objects.filter(worker__user = request.user, project=requested_project).exists()
            data.update({'is_project_stackholder': is_project_stackholder, 'is_project_member': is_project_member})
        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserModelView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated, IsRoleOwnRoot, AdminOnly]
    
