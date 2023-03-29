import datetime, uuid
from django.db import models
from django.utils.crypto import get_random_string as rnd
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    usertype = models.CharField(choices = [('d','Doctor'), ('p','Patient')], max_length=1, default='p')
    class Meta: 
        permissions=[('is_user', 'Is User'),]

        
class Person(models.Model):  #  Abstract Model 
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    slug = models.SlugField(null=True, editable=False)
    class Meta:
        abstract=True

    @property
    def full_name(self):
        "Returns full name of Person"
        return f'{self.user.first_name} {self.user.last_name}'
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.full_name+ "-" + rnd(7))

        return super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.slug}'
        
    
class Patient(Person):
    adress=models.CharField(max_length=80)
    class Meta: 
        permissions=[('is_patient', 'Is Patient'),]

      
class Doctor(Person):
    specialization=models.CharField(max_length=12)
    class Meta: 
        permissions=[('is_doctor','Is Doctor'),]


class Category(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name=models.CharField(max_length=30, unique=True, default='')
    class Meta:
        ordering=('name',)

    def __str__(self):
        return f'{self.name}'


class Visit(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title=models.CharField(max_length=100, default='')
    date=models.DateTimeField(default=datetime.date.today)    
    patient=models.ForeignKey(Patient, models.PROTECT, default='')
    doctor=models.ForeignKey(Doctor, models.PROTECT, default='')
    category=models.ForeignKey(Category,models.PROTECT,null=True,blank=True, default='')
    description=models.TextField()
    price=models.CharField(max_length=10)
    class Meta:
        ordering=('date',)

    def __str__(self):
        return f' Visit date: {self.date}, Price: {self.title}'
