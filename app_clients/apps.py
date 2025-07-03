from django.apps import AppConfig

class AppClientsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_clients'

    def ready(self):
        import app_clients.signals
