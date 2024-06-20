from django.db.models import Model, ForeignKey, CharField, URLField, DateField, PROTECT, CASCADE
from logs.middleware import current_request
from statuses.models.layer_status import ChangeLayerStatus
from comments.models import Comment
from django.contrib.contenttypes.fields import GenericRelation
from dirtyfields import DirtyFieldsMixin


class Layer(DirtyFieldsMixin, Model):
    project = ForeignKey('projects.Project', on_delete=CASCADE)
    name = CharField(max_length=20)
    description = CharField(max_length=1000, blank=True)
    link_to_project_in_git = URLField(null=True, blank=True)
    link_to_project_in_ser_reg = URLField(null=True, blank=True)
    layer_type = ForeignKey('references.LayerType', on_delete=PROTECT)
    status = ForeignKey('statuses.Status', on_delete = PROTECT)
    expected_testbed_start_date = DateField(null=True, blank=True)
    complexity = ForeignKey('references.Complexity', on_delete=PROTECT)
    stack = ForeignKey('projects.Stack', on_delete = PROTECT)
    history = GenericRelation("logs.HistoryOfChange")

    class Meta:
        app_label = 'projects'

    def save(self, *args, **kwargs):
        comment = kwargs.pop('comment', None)

        # Logging project with an updated "state"
        if self.pk is not None:
            old_status = Layer.objects.get(pk=self.pk).status
            if old_status != self.status:
                if comment == '':
                    comment_instance = None
                else: 
                    comment_instance = Comment.objects.create(
                        project=self.project,
                        layer = self,
                        text = comment,
                        created = current_request().user,
                    )
                # Create ChangeLayerState instance for logging
                new_state_inst= ChangeLayerStatus(
                    layer=self,
                    status=self.status,
                    comment=comment_instance,
                    installed=current_request().user
                )
                new_state_inst.save()

        self.full_clean()
        
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"