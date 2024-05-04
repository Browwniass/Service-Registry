from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from logs.models import HistoryOfChange
from .middleware import current_request
import json
from django.utils import timezone

@receiver(post_delete)
@receiver(post_save)
def log_model_change(sender, instance, **kwargs):
    if current_request()!=None:
        content_type = ContentType.objects.get_for_model(sender)
        acceptable_apps = ['projects', 'comments', 'teams', 'references']
        if content_type.app_label in acceptable_apps:#Checking for relevance to my models
            if (kwargs['signal'] == post_save or kwargs['signal'] == post_delete ):
                json_data = json.dumps(model_to_dict(instance), default=str)#Conversion to json
                #Saving to history
                HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))


