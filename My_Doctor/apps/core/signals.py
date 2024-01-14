from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (Doctor, Director, Patient, 
                     User, VisitImageFile)


def create_usertype(sender, instance, created, **kwargs):
    if created:
        if instance.usertype =='p':
            Patient.objects.create(user=instance)
            instance.type_created = True
            instance.save()
        if instance.usertype =='d':
            Doctor.objects.create(user=instance)
            instance.type_created = True
            instance.save()
        if instance.usertype =='c':
            Director.objects.create(user=instance)
            instance.type_created = True
            instance.save()
      
post_save.connect(create_usertype, sender=User)


def update_usertype(sender, instance, created, **kwargs):
    if not created:
        if instance.user.type_updated == False:
            instance.user.type_updated = True
            instance.user.save()
      
post_save.connect(update_usertype, sender=Patient)
post_save.connect(update_usertype, sender=Doctor)
post_save.connect(update_usertype, sender=Director)


# @receiver(pre_save, sender=VisitImageFile)
# def get_user_image_path(sender, instance, **kwargs):
#         ...
#         print('signals')
    
       
# @receiver(pre_save, sender=VisitImageFile)
# def get_user_thumb_path(sender, instance, **kwargs):
#         ...
