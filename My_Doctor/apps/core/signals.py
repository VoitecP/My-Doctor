from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import (Doctor, Director, Patient, 
                     User, VisitImageFile)




# def user_update_usertype(sender, instance, created, **kwargs):
#     if created == False:
#         print('if created false')
#         if instance.type_updated == False:
#             print('if isntance  type updaed false')
#             instance.type_updated = True
#             instance.save()

   
# # # Todo temporary signal
# post_save.connect(user_update_usertype, sender=User)


def create_usertype(sender, instance, created, **kwargs):
    if created == True:
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

    # if created == False:
    #     if instance.type_updated == False:
    #         # print('if isntance  type updaed false')
    #         instance.type_updated = True
    #         instance.save()
      
post_save.connect(create_usertype, sender=User)


def update_usertype(sender, instance, created, **kwargs):
    if not created:
        if instance.user.type_updated == False:
            instance.user.type_updated = True
            instance.user.save()
      
post_save.connect(update_usertype, sender=Patient)
post_save.connect(update_usertype, sender=Doctor)
post_save.connect(update_usertype, sender=Director)



# def user_update_usertype(sender, instance, created, **kwargs):
#     if created == False:
#         print('if created false')
#         if instance.type_updated == False:
#             print('if isntance  type updaed false')
#             instance.type_updated = True
#             instance.save()

   
# # # Todo temporary signal
# post_save.connect(user_update_usertype, sender=User)

# @receiver(pre_save, sender=VisitImageFile)
# def get_user_image_path(sender, instance, **kwargs):
#         ...
#         print('signals')
    
       
# @receiver(pre_save, sender=VisitImageFile)
# def get_user_thumb_path(sender, instance, **kwargs):
#         ...
