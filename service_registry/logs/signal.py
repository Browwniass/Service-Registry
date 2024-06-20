from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.forms import model_to_dict
from logs.models import HistoryOfChange
from projects.models.stack import Stack
from .middleware import current_request
import json
from django.utils import timezone
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


ACCEPTABLE_APPS = ['projects', 'comments', 'teams', 'references']
EXCEPTION_MODELS = ['status'] # Models in excluded apps, that needed to be tracked
M2M_MODELS = ['Stack'] # Models that had fields with m2m relation


@receiver(post_save)
def log_model_change(sender, instance, created, **kwargs):
    """
    Signal for saving changes in model.
    When creating a model, saved all of it fields.
    """
    content_type = ContentType.objects.get_for_model(sender)# Check user model

    if content_type.app_label in ACCEPTABLE_APPS or content_type.model in EXCEPTION_MODELS: # Checking if its signal belong to tracked models
        instance.is_created = created
        if not created:            
            changed_fields = instance.get_dirty_fields(check_relationship=True) # Dict with changed fields and their values
            new_dict = {} # new dict
            for field, value in changed_fields.items():
                new_dict[field] = getattr(instance, field)
            instance_dict = {'action': 'PUT', 'changes': new_dict}       
        elif created:
            if  sender.__name__ in M2M_MODELS:
                return # Full instance data can be saved in m2m_changed
            
            # Writing changes in dict, model info, making values readable using the meta method for models
            instance_dict = {'action': 'CREATE' , 'changes': {field.name: getattr(instance, field.name) for field in instance._meta.fields}}
            instance.is_created = False

        json_data = json.dumps(instance_dict, default=str, ensure_ascii=False) # Conversion to json
        # Saving to history  
        log = HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
        instance.key = log.pk


@receiver(post_delete)
def log_model_change(sender, instance, **kwargs):
    """
    Signal to save model values before deleting
    """
    content_type = ContentType.objects.get_for_model(sender)
    # Checking for relevance to my models
    if content_type.app_label in ACCEPTABLE_APPS or content_type.model in EXCEPTION_MODELS: 
        instance_dict = {field.name: getattr(instance, field.name) for field in instance._meta.fields}
        # M2m fields are not present in the instance provided by the signal, so they need to be processed separately
        if sender.__name__ in M2M_MODELS:
            # Get a list of m2m fields in model and retrieve them
            m2m_fields = [field for field in instance._meta.get_fields() if field.many_to_many]
            dirty = instance.get_dirty_fields(check_m2m={field.name: [] for field in m2m_fields})

            for field_name, ids in dirty.items():
                # Get the model referenced by the M2M field
                related_model = instance._meta.get_field(field_name).related_model
                elements_instances = []

                for element_id in ids:
                    element_instance = related_model.objects.get(pk=element_id)
                    elements_instances.append(element_instance)
                instance_dict[field_name] = elements_instances
            
        instance_dict = {'action': 'DELETE' , 'changes': instance_dict}
        json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)
        HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
            

@receiver(m2m_changed, sender=Stack.elements.through)
def log_m2m_change(sender, instance, action, **kwargs):
    """
    Signal for saving changes in model with m2m fields.
    """
    if action in ['post_add', 'post_remove']:
        # The is_created attribute determines whether a new instance has been created or modified
        if hasattr(instance, 'is_created') and getattr(instance, 'is_created', True): 
            instance_dict = {'action': 'CREATE' , 'changes': model_to_dict(instance)}
            instance.is_created = False
            json_data = json.dumps(instance_dict, default=str, ensure_ascii=False)
            HistoryOfChange.objects.create(content_object=instance, value=json_data, changer=current_request().user, date=timezone.localtime(timezone.now()))
        else:
            # By the value of the transmitted key, when saving the change history, 
            # we get a HistoryOfChange model that stores it, in order to append 
            # it later with the value of the changed m2m fields
            if  hasattr(instance, 'key'):
                key = getattr(instance, 'key', True)
                val = instance.history.get(pk=key) # Get HistoryOfChange model
                dict_val = json.loads(val.value)
                dict_val['changes']['elements'] = model_to_dict(instance)['elements']

                json_data = json.dumps(dict_val, default=str, ensure_ascii=False)
                val.value = json_data # Updating m2m field for last history instance
                val.save()