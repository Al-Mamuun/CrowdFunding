from django.apps import AppConfig

class HomeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'HomeAPP'

    def ready(self):
        import HomeAPP.signals 
        
