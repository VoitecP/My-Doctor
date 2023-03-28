from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    usertype = models.CharField(choices = [('d','Doctor'), ('p','Patient')], max_length=1)

    # def save(self, *args, **kwargs) :
    #     super().save(*args, **kwargs)
    #     if self.usertype=='p':
    #         pass
    #     if self.usertype=='d':
    #         pass    
            




class Person(models.Model):  #  Abstract Model 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    class Meta:
        abstract=True
        
    
    
    
    


    
    
class Patient(Person):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  
    citizen_id=models.CharField(max_length=11)
    adress=models.CharField(max_length=80)
    city=models.CharField(max_length=20)
    zip_code=models.CharField(max_length=5)
   
        
    

class Doctor(Person):
    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    specialization=models.CharField(max_length=12)
    # objects=models.Manager()