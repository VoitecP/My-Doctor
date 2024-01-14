import  datetime
from django.db import models
from django.utils.crypto import get_random_string as rnd
from django.template.defaultfilters import slugify

from rest_framework.serializers import ValidationError


from .user import User


class Person(models.Model):  #  Abstract Model 
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    slug=models.SlugField(null=True, editable=False)
    phone=models.CharField(default='', max_length=50)

    class Meta:
        abstract=True

    def get_absolute_url(self):
        return f"/api/test/{self.pk}/"
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.full_name+ "-" + rnd(7))
        return super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.slug}'
        
    @property
    def url(self):
        return self.get_absolute_url()
    

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    
class Patient(Person):
    adress=models.CharField(max_length=80)
    birth_date=models.DateField(default=datetime.date.today)
    
    class Meta: 
        permissions=[('is_patient', 'Is Patient'),]



class Doctor(Person):
    specialization=models.CharField(max_length=12)
    private_field=models.CharField(max_length=50, default='private')    # temporary field


    def save(self, *args, **kwargs):
        # sometring wrong
        # self.__class__.objects.exclude(user_id=self.user.id).delete()
        super(Doctor, self).save(*args, **kwargs)
    
    
    class Meta: 
        permissions=[('is_doctor','Is Doctor'),]


class Director(Person):
    description=models.CharField(max_length=100, default='')
    private_info=models.CharField(max_length=500, default='')
    # _singleton = models.BooleanField(default=True, editable=False, unique=True)
     
    class Meta: 
        permissions=[('is_director','Is Director'),]


    def save(self, *args, **kwargs):
        if not self.pk and Director.objects.exists():
            raise ValidationError('Only one Director instance is allowed')
        return super(Director, self).save(*args, **kwargs)