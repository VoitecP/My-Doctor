from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    
    # name = 'core'
    label='core'
    name = 'apps.core'

    # signals config
    def ready(self):
        import apps.core.signals
        