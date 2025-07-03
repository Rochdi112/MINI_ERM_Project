from django.apps import AppConfig

class AppMaterielsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_materiels'

    def ready(self):
        import app_materiels.signals
