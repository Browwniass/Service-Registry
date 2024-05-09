from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from logs.models import HistoryOfChange
from projects.serializers.stack import StackSerializer
from projects.models.stack import Stack
from .middleware import current_request
import json
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.dispatch import Signal

execute_log_model_change = True

signal_information_received = Signal()

@receiver(signal_information_received)
def process_information(sender, **kwargs):
    # Получаем информацию
    info = kwargs['info']
    # Выполняем необходимые действия
    print("Received information:", info)


@receiver(post_delete)
@receiver(post_save)
def log_model_change(sender, instance, **kwargs):
    if current_request()!=None and not(current_request().user.is_anonymous):
        content_type = ContentType.objects.get_for_model(sender)
        acceptable_apps = ['projects', 'comments', 'teams', 'references']
        if content_type.app_label in acceptable_apps:#Checking for relevance to my models
            if (kwargs['signal'] == post_save or kwargs['signal'] == post_delete ):
                json_data = json.dumps(model_to_dict(instance), default=str, ensure_ascii=False)#Conversion to json
                #Saving to history
                new_log = HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
                signal_information_received.send(sender=None, info=new_log.id)

# In case m2m update last history instance, cause thath rel didn`t catch by log_model_change signal
@receiver(m2m_changed,  sender=Stack.elements.through)
def log_m2m_change(sender, instance, action, **kwargs):
    if current_request()!=None and not(current_request().user.is_anonymous):
        if action in ['post_add', 'post_remove']:
            val = instance.history.last()# Get last history instance   
            json_data = json.dumps(model_to_dict(instance), default=str, ensure_ascii=False)# Conversion to json
            val.value=json_data# Updating m2m field for last history instance
            val.save()
            

