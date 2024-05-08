from django.utils import timezone
from rest_framework import viewsets
from projects.models.quarter import Quarter
from projects.serializers.quarter import QuarterChoicesSerializer, QuarterSerializer 
from config.permissions import AdminOnly


class QuarterModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Quarter.objects.all()
    serializer_class = QuarterSerializer
    permission_classes = [AdminOnly]
    
class QuarterChoicesModelView(viewsets.ReadOnlyModelViewSet):
    queryset = Quarter.objects.all()
    serializer_class = QuarterChoicesSerializer

    def get_queryset(self):
        current_year = timezone.localtime(timezone.now()).year
        return Quarter.objects.filter(year__gte=current_year)