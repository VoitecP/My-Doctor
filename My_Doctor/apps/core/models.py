import uuid, datetime
from django.db import models
from django.utils.crypto import get_random_string as rnd
from django.template.defaultfilters import slugify
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    usertype=models.CharField(choices = [('d','Doctor'), ('p','Patient'), ('c','Director'),], max_length=1, default='')  # ,('c','Director'),  By Admin
    # first_name  (Heritated from AbstractUser)
    # last_name
    # email
    
    class Meta: 
        permissions=[('is_user', 'Is User'),]  # what to do with that ?
        managed = True

        
class Person(models.Model):  #  Abstract Model 
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    slug=models.SlugField(null=True, editable=False)
    phone=models.CharField(default='', max_length=50)

    class Meta:
        abstract=True

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.full_name+ "-" + rnd(7))
        return super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.slug}'
        
    
class Patient(Person):
    adress=models.CharField(max_length=80)
    birth_date=models.DateField(default=datetime.date.today)
    
    class Meta: 
        permissions=[('is_patient', 'Is Patient'),]

      
class Doctor(Person):
    specialization=models.CharField(max_length=12)
    private_field=models.CharField(max_length=50, default='private')    # temporary field


    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(Doctor, self).save(*args, **kwargs)
    
    class Meta: 
        permissions=[('is_doctor','Is Doctor'),]


class Director(Person):
    description=models.CharField(max_length=12)
    
    class Meta: 
        permissions=[('is_director','Is Director'),]



class Category(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name=models.CharField(max_length=30, unique=True, default='')
    description=models.TextField(default='')

    class Meta:
        ordering=('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'


class Visit(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title=models.CharField(max_length=100, default='')
    date=models.DateTimeField(default=None, null=True, blank=True)    
    patient=models.ForeignKey(Patient, models.PROTECT, default=None)
    doctor=models.ForeignKey(Doctor, models.PROTECT, default=None)
    category=models.ForeignKey(Category,models.PROTECT,null=True,blank=True, default=None)
    description=models.TextField()
    price=models.CharField(max_length=10)
    
    class Meta:
        ordering=('date',)

    def __str__(self):
        format= f'{self.date}'
        return f' Visit: {format[0:10]} - {self.title}'



