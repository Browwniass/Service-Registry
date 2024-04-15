import sys
from project_catalog.models import *
from project_catalog.serializers import *
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
#from .permissions import IsFullOrOther
from rest_framework import generics
from rest_framework.decorators import action
from django.db.models.fields.related import ForeignKey
from .utils import getRelatedFields
#from .metadata import OptionWithChoices
from .permissions import *
import datetime
from django.utils import timezone
from rest_framework import viewsets

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'email': user.email, 'role': user.role})
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Successfully logged out.'})
    

#Вывод Приоритетов
class PriorityAPIList(generics.ListCreateAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

#Редактирование Приоритетов
class PriorityAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

#Вывод ProjectType
class ProjectTypeAPIList(generics.ListCreateAPIView):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer

#Редактирование ProjectType
class ProjectTypeAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer

#Вывод TeamMemberRole
class TeamMemberRoleAPIList(generics.ListCreateAPIView):
    queryset = TeamMemberRole.objects.all()
    serializer_class = TeamMemberRoleSerializer

#Редактирование TeamMemberRole
class TeamMemberRoleAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeamMemberRole.objects.all()
    serializer_class = TeamMemberRoleSerializer

#Вывод ProjectComplexity
class ProjectComplexityAPIList(generics.ListCreateAPIView):
    queryset = ProjectComplexity.objects.all()
    serializer_class = ProjectComplexitySerializer

#Редактирование ProjectComplexity
class ProjectComplexityAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectComplexity.objects.all()
    serializer_class = ProjectComplexitySerializer

#Вывод LayerType
class LayerTypeAPIList(generics.ListCreateAPIView):
    queryset = LayerType.objects.all()
    serializer_class = LayerTypeSerializer

#Редактирование LayerType
class LayerTypeAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LayerType.objects.all()
    serializer_class = LayerTypeSerializer

#Вывод ProjectState
class ProjectStateAPIList(generics.ListCreateAPIView):
    queryset = ProjectState.objects.all()
    serializer_class = ProjectState

#Редактирование ProjectState
class ProjectStateAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectState.objects.all()
    serializer_class = ProjectStateSerializer

#Вывод Quarter
class QuarterAPIList(generics.ListCreateAPIView):
    permission_classes = (IsAdminOrReadOnly,) 
    queryset = Quarter.objects.all()
    serializer_class = QuarterSerializer

#Редактирование Quarter
class QuarterAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminOrReadOnly, ) 
    queryset = Quarter.objects.all()
    serializer_class = QuarterSerializer


class ProjectAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    #Getting all possible options to select in fields that involve selecting from existing table values    @action(detail=False, methods=['get'])
    @action(detail=False, methods=['get'])
    def list_choice_data(self, request):
        model = self.queryset.model
        nested_serializers = getRelatedFields(model)#Getting all the options for a given model
        return Response({'choices': nested_serializers})#Sending
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        comments = instance.comment.all()
        history = instance.history.all()    
        comments_serializer = CommentSerializer(instance=comments, many=True)   
        history_serializer = HistoryOfChangeSerializer(instance=history, many=True)
        return Response({'project': serializer.data,
                         'comments': comments_serializer.data,
                         'history': history_serializer.data})

    def get_queryset(self):
        if not(self.request.user.is_anonymous):
            try:
                is_team_member = TeamMember.objects.get(user=self.request.user)
            except TeamMember.DoesNotExist:
                is_team_member = None
            #Filtering by "state"
            if 'state' in self.request.query_params and (is_team_member or self.request.user.role == User.ROLE_CHOICES[0][0]):
                state = self.request.query_params['state']
                
                return Project.objects.filter(state__name=state)
        return Project.objects.all()
    
              
class LayerAPI(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class = LayerSerializer

#Вывод Observer
class ObserverAPI(viewsets.ModelViewSet):
    queryset = Observer.objects.all()
    serializer_class = ObserverSerializer

#Вывод Приоритетов
class CommentAPIList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    #Hiding a "deleted" comment
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_hidden = True
        instance.date_delete = timezone.localtime(timezone.now())
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)  # Ответ, указывающий на успешное удаление
    
#Вывод CommentsFile
class CommentsFileAPIList(generics.ListCreateAPIView):
    queryset = CommentsFile.objects.all()
    serializer_class = CommentsFileSerializer

#Редактирование CommentsFile
class CommentsFileAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CommentsFile.objects.all()
    serializer_class = CommentsFileSerializer

#Вывод ProjectDocument
class ProjectDocumentAPIList(generics.ListCreateAPIView):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer

#Редактирование ProjectDocument
class ProjectDocumentAPIDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectDocument.objects.all()
    serializer_class = ProjectDocumentSerializer


class UserAPI(viewsets.ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class HistoryOfChangeAPI(viewsets.ModelViewSet):
    permission_classes = [AdminOnly]
    queryset = HistoryOfChange.objects.all()
    serializer_class = HistoryOfChangeSerializer

#Вывод TeamMember
class TeamMemberAPIList(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer

    #Getting all possible options to select in fields that involve selecting from existing table values    @action(detail=False, methods=['get'])
    @action(detail=False, methods=['get'])
    def list_choice_data(self, request):
        model = self.queryset.model
        nested_serializers = getRelatedFields(model)#Getting all the options for a given model
        return Response({'choices': nested_serializers})#Sending
