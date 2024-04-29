from django.db.models import Model, ForeignKey, DateTimeField, PROTECT, CASCADE, SET_NULL

#Объект хранит информацию присущую истории изменений статуса проекта
class ChangeLayerStatus(Model):
    layer = ForeignKey('projects.Layer', on_delete = CASCADE)
    status = ForeignKey('statuses.Status', on_delete = PROTECT)
    comment = ForeignKey('comments.Comment', on_delete = SET_NULL, null=True, blank=True)
    date_installation = DateTimeField(auto_now=True, unique=True)
    installed = ForeignKey('teams.User', on_delete = SET_NULL, null=True, blank=True)
        
    class Meta:
        app_label = 'statuses'

    def __str__(self):
        return f"{self.layer}[{self.date_installation}]"
    