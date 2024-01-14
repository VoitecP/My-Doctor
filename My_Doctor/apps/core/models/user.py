import uuid
from django.db import models
from django.utils.crypto import get_random_string as rnd

from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    PATIENT = 'p'
    DOCTOR = 'd'
    DIRECTOR = 'c'
    CHOICES = [
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        #(DIRECTOR, 'Director'), 
    ]

    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    usertype=models.CharField(choices = CHOICES, max_length=1, default='') 
    type_created=models.BooleanField(default=False, editable=False)
    type_updated=models.BooleanField(default=False, editable=False)
    # date_created=models.DateTimeField(default=timezone.now, editable=False)
    ## Heritated from AbstractUser
    # first_name  
    # last_name
    # email
    


    class Meta: 
        permissions=[('is_user', 'Is User'),]  # what to do with that ?
        managed = True



    