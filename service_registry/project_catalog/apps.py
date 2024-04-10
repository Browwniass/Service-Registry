from django.apps import AppConfig


class ProjectCatalogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'project_catalog'

    def ready(self):
        import project_catalog.signals
        import project_catalog.metadata
