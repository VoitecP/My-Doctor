from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Patient, Doctor, Director

# doctor create works
def create_doctor(sender, instance, created, **kwargs):
    if created:
        print('some created')
        if instance.usertype=='p':
                print('patient created')
        if instance.usertype=='d':
                print('doctor created')
        # Doctor.objects.create(user=user)

post_save.connect(create_doctor, sender=User)



##

# models:

# class Profile(models.model):
#     user=models.OnetoOne(User, on delete
#                         )
#     first_name=
#     last+name


# def create_profile():
#     if created:
#         Profile.object.create(..)
#         print('created')

post_save.connect(create_doctor, sender=User )

# def update_profile():
#     if created== False:
#       instance.profile.save()
#         print()
#         try:
#             instance.profile.save()
#             print()
#         execpt:
#             profile.objects.create()
#             print()

# post_save.connect(update_doctor, sender=User )