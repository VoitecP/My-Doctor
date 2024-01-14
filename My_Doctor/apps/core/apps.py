from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # name = 'core'
    label='core'
    name = 'apps.core'

    # signals config

    def ready(self):
        
        import apps.core.signals
        #from . import signals

        # from django.db.models.signals import pre_save
        # from .models import VisitImageFile
        # pre_save.connect(apps.core.signals.get_user_image_path, sender=VisitImageFile)
        # pre_save.connect(apps.core.signals.get_user_thumb_path, sender=VisitImageFile)