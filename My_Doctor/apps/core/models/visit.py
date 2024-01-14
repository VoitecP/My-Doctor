import uuid

from django.db import models

from apps.core.models import (Category, Doctor, Patient, 
                              models_manager, storage)


class Visit(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title=models.CharField(max_length=100, default='')
    date=models.DateTimeField(default=None, null=True, blank=True)    
    patient=models.ForeignKey(Patient, models.PROTECT, default=None)
    doctor=models.ForeignKey(Doctor, models.PROTECT, default=None)
    category=models.ForeignKey(
        Category,models.PROTECT,
        null=True,blank=True, default=None)    
    image=models.ImageField(
        upload_to=storage.user_image_path, validators=[storage.ext_validator], 
        blank=True, default='')
    description=models.TextField()
    price=models.CharField(max_length=10)
    closed=models.BooleanField(default=False)
    
    objects=models.Manager()  
    year_objects=models_manager.VisitYearSummary()
    month_objects=models_manager.VisitMonthSummary()
    category_objects=models_manager.VisitCategorySummary()
    doctor_objects=models_manager.VisitDoctorSummary()
    
    class Meta:
        ordering=('date',)

    def __str__(self):
        format= f'{self.date}'
        return f' Visit: {format[0:10]} - {self.title}'
    
    def get_absolute_url(self):
        # Todo Url check, or delete
        return f"/api/visit-test/{self.pk}/"
    
    @property
    def url(self):
        return self.get_absolute_url()
