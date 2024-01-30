import factory
from factory.django import DjangoModelFactory
from .models import Category, User, Patient, Doctor, Visit, VisitImageFile, Director
from django.db.models.signals import post_save
from datetime import datetime

class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Visit Category {n}')  
    # description = factory.Faker('sentence', nb_words=20)
    description = factory.Faker('text')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):

        while True:
            try:
                return super()._create(model_class, *args, **kwargs)
            except:
                kwargs['name'] = factory.Sequence(lambda n: f'Visit Category {n + 1}')

   
@factory.django.mute_signals(post_save)
class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient

    #user = factory.SubFactory(UserPatientFactory)
    user = factory.SubFactory('apps.core.factories.UserPatientFactory', patient=None)
    slug = factory.Faker('slug')
    phone = factory.Faker('phone_number')
    adress = factory.Faker('address')
    birth_date = factory.Faker('date_of_birth', minimum_age=5, maximum_age=85) 
  

@factory.django.mute_signals(post_save)
class UserPatientFactory(DjangoModelFactory):
    class Meta:
        model = User
   
    username = factory.Sequence(lambda n: f'user-patient-{n:02d}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    usertype = 'p'
    password = factory.django.Password('password1234')
    patient = factory.RelatedFactory(PatientFactory, factory_related_name='user')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        while True:
            try:
                return super()._create(model_class, *args, **kwargs)
            except :
                kwargs['username'] = factory.Sequence(lambda n: f'user-patient-{n + 1:02d}')


@factory.django.mute_signals(post_save)
class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = Doctor

    #user = factory.SubFactory(UserPatientFactory)
    user = factory.SubFactory('apps.core.factories.UserDoctorFactory', doctor=None)
    slug = factory.Faker('slug')
    phone = factory.Faker('phone_number')
    specialization = factory.Faker('text')
    private_field = factory.Faker('text') 
    

@factory.django.mute_signals(post_save)
class UserDoctorFactory(DjangoModelFactory):
    class Meta:
        model = User
   
    username = factory.Sequence(lambda n: f'user-doctor-{n:02d}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    usertype = 'd'
    password = factory.django.Password('password1234')
    doctor = factory.RelatedFactory(DoctorFactory, factory_related_name='user')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        while True:
            try:
                return super()._create(model_class, *args, **kwargs)
            except :
                kwargs['username'] = factory.Sequence(lambda n: f'user-doctor-{n + 1:02d}')


@factory.django.mute_signals(post_save)
class DirectorFactory(DjangoModelFactory):
    class Meta:
        model = Director

    #user = factory.SubFactory(UserPatientFactory)
    user = factory.SubFactory('apps.core.factories.UserDirectorFactory', director=None)
    slug = factory.Faker('slug')
    phone = factory.Faker('phone_number')
    
    description = factory.Faker('text')
    private_info = factory.Faker('text')


@factory.django.mute_signals(post_save)
class UserDirectorFactory(DjangoModelFactory):
    class Meta:
        model = User
   
    username = factory.Sequence(lambda n: f'user-director-{n:02d}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    usertype = 'c'
    password = factory.django.Password('password1234')
    director = factory.RelatedFactory(DirectorFactory, factory_related_name='user')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        while True:
            try:
                return super()._create(model_class, *args, **kwargs)
            except :
                kwargs['username'] = factory.Sequence(lambda n: f'user-director-{n + 1:02d}')


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
   
    username = factory.Sequence(lambda n: f'user-patient-{n:02d}')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    usertype = 'p'
    password = factory.django.Password('password1234')

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
       
        while True:
            try:
                return super()._create(model_class, *args, **kwargs)
            except :
                username = factory.Sequence(lambda n: f'user-patient-{n + 1:02d}')


# patients = PatientFactory.create_batch(10)


class VisitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visit

    title = factory.Faker('sentence', nb_words=3)
    patient = factory.Iterator(Patient.objects.all())
    doctor = factory.Iterator(Doctor.objects.all())
    category = factory.Iterator(Category.objects.all())
    date = factory.Faker('date_time_between', start_date=datetime(2018, 1, 1), end_date=datetime(2023, 12, 31))
    description = factory.Faker('paragraph')
    price = factory.Faker('random_int', min=10, max=600)
    closed = factory.Faker('boolean')
    #image = factory.Iterator(VisitImageFile.objects.all())


class Visit2Factory(factory.django.DjangoModelFactory):
    class Meta:
        model = Visit

    title = factory.Faker('sentence', nb_words=3)
    patient = factory.Iterator(Patient.objects.all())
    doctor = factory.Iterator(Doctor.objects.all())
    #category = factory.Iterator(Category.objects.all())
    date = factory.Faker('date_time_between', start_date=datetime(2018, 1, 1), end_date=datetime(2023, 12, 31))
    description = factory.Faker('paragraph')
    price = factory.Faker('random_int', min=10, max=600)
    closed = factory.Faker('boolean')
    #image = factory.Iterator(VisitImageFile.objects.all())



class ImageFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VisitImageFile

    visit = factory.Iterator(Visit.objects.all())
    image = factory.django.ImageField(filename='example.jpg', width=1024, height=768)
    #thumb = factory.django.ImageField(filename='thumb.jpg', width=200, height=200)