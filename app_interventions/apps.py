from django.apps import AppConfig

class AppInterventionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_interventions'

    def ready(self):
        import app_interventions.signals
