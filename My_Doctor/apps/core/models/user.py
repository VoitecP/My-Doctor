import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    CHOICES = {
        'p':'Patient',
        'd': 'Doctor',
        'c': 'Director', 
    }
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    usertype=models.CharField(choices = CHOICES.items(), max_length=1, default='') 
    type_created=models.BooleanField(default=False, editable=False)
    type_updated=models.BooleanField(default=False)
    ## Heritated from AbstractUser
    # first_name  
    # last_name
    # email
    
    class Meta: 
        permissions=[('is_user', 'Is User'),]  # what to do with that ?
        managed = True



    