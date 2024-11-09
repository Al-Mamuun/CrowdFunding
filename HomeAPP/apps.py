from django.apps import AppConfig

class HomeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HomeAPP'

    def ready(self):
        import HomeAPP.signals  # Ensure this is at the bottom to connect signals

