from django.apps import AppConfig

class AppRapportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_rapports'

    def ready(self):
        import app_rapports.signals
