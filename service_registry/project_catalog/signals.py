from urllib import request
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict

from .serializers import ProjectSerializer
from .models import ChangeLayerState, ChangeProjectState, HistoryOfChange, CommentsFile, Project
from .middleware import current_request
from django.core.serializers import serialize
import json
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser
import json

@receiver(post_delete)
@receiver(post_save)
def log_model_change(sender, instance, **kwargs):
    content_type = ContentType.objects.get_for_model(sender)

    if content_type.app_label == 'project_catalog':
        not_logging_sender = [HistoryOfChange, ChangeLayerState, ChangeProjectState]
        print(sender)
        if (kwargs['signal'] == post_save or kwargs['signal'] == post_delete ) and not(sender in not_logging_sender):
            json_data = json.dumps(model_to_dict(instance), default=str)
            HistoryOfChange.objects.create(content_object=content_type, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
    