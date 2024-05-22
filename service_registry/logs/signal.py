from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from logs.models import HistoryOfChange
from projects.serializers.stack import StackSerializer
from projects.models.stack import Stack, StackElement
from .middleware import current_request
import json
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


@receiver(post_save)
def log_model_change(sender, instance, created, **kwargs):
    if current_request()!=None and not(current_request().user.is_anonymous):
        content_type = ContentType.objects.get_for_model(sender)
        acceptable_apps = ['projects', 'comments', 'references']
        exception_models = ['status']
        #print(content_type.model=='status')
        if content_type.app_label in acceptable_apps or content_type.model in exception_models: #Checking for relevance to my models 
            instance.is_created = created
            if not created:            
                changed_fields = instance.get_dirty_fields(check_relationship=True)# Словарь измененных полей 
                new_dict = {}# Новый словарь
                for field, value in changed_fields.items():
                    new_dict[field] = getattr(instance, field)
                #instance_dict = {'action': 'PUT', 'changes': {'new': new_dict, 'old': changed_fields}}    
                instance_dict = {'action': 'PUT', 'changes': new_dict}       
            elif created:
                if  sender.__name__ == 'Stack':
                    return
                instance_dict = {'action': 'CREATE' , 'changes': {field.name: getattr(instance, field.name) for field in instance._meta.fields}}
                instance.is_created = False

            json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)#Conversion to json
            #Saving to history  
            log = HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
            instance.key = log.pk


@receiver(post_delete)
def log_model_change(sender, instance, **kwargs):
    if current_request()!=None and not(current_request().user.is_anonymous):
        content_type = ContentType.objects.get_for_model(sender)
        acceptable_apps = ['projects', 'comments', 'teams', 'references']
        exception_models = ['status']
        if content_type.app_label in acceptable_apps or content_type.model in exception_models:#Checking for relevance to my models
            instance_dict = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
            if sender.__name__ == 'Stack':
                dirty = instance.get_dirty_fields(check_m2m={"elements": []})
                elements_ids = dirty['elements']
                elements_instances = []
                for element_id in elements_ids:
                    element_instance = StackElement.objects.get(pk=element_id)
                    elements_instances.append(element_instance)
                instance_dict['elements'] = elements_instances
                
            instance_dict = {'action': 'DELETE' , 'changes': instance_dict}
            json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)#Conversion to json
            #Saving to history
            HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
            

# In case m2m update last history instance, cause thath rel didn`t catch by log_model_change signal
@receiver(m2m_changed, sender=Stack.elements.through)
def log_m2m_change(sender, instance, action, **kwargs):
    if current_request()!=None and not(current_request().user.is_anonymous):
        if action in ['post_add', 'post_remove']:
            if hasattr(instance, 'is_created') and  getattr(instance, 'is_created', True): 
                instance_dict = {'action': 'CREATE' , 'changes': model_to_dict(instance)}
                instance.is_created = False
                json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)#Conversion to json
                HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
            else:
                if  hasattr(instance, 'key'):
                    key = getattr(instance, 'key', True)
                    val = instance.history.get(pk=key)
                    dict_val = json.loads(val.value)
                    #print(model_to_dict(instance)['elements'])
                    dict_val['changes']['elements'] = model_to_dict(instance)['elements']
                    json_data = json.dumps(dict_val, default=str, ensure_ascii=False)# Conversion to json
                    val.value=json_data# Updating m2m field for last history instance
                    val.save()
                else:
                    instance_dict = {'action': 'PUT' , 'changes': model_to_dict(instance)['elements']}
                    json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)#Conversion to json
                    HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
            
            
        
"""            key = getattr(instance, 'key', True)
            val = instance.history.get(pk=key)
            dict_val = json.loads(val.value)
            
        instance.created = False
        """
"""            val = instance.history.last()# Get last history instance   
            json_data = json.dumps(model_to_dict(instance), default=str, ensure_ascii=False)# Conversion to json
            val.value=json_data# Updating m2m field for last history instance
            val.save()"""
            

