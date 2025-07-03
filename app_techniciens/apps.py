from django.apps import AppConfig

class AppTechniciensConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_techniciens'

    def ready(self):
        import app_techniciens.signals
