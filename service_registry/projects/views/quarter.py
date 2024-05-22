from django.utils import timezone
from rest_framework import viewsets
from projects.models.quarter import Quarter
from projects.serializers.quarter import QuarterChoicesSerializer, QuarterSerializer 
from config.permissions import AdminOnly
from rest_framework.permissions import IsAuthenticated


class QuarterModelView(viewsets.ModelViewSet):
    queryset = Quarter.objects.all()
    serializer_class = QuarterSerializer
    permission_classes = [IsAuthenticated, AdminOnly]
    
class QuarterChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Quarter.objects.all()
    serializer_class = QuarterChoicesSerializer

    def get_queryset(self):
        current_year = timezone.localtime(timezone.now()).year
        return Quarter.objects.filter(year__gte=current_year)