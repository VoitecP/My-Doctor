import uuid

from django.db import models


class Category(models.Model):
    id=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name=models.CharField(max_length=30, unique=True, default='')
    description=models.TextField(default='')

    class Meta:
        ordering=('name',)
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f"/api/category-test/{self.pk}/"
    
    @property
    def url(self):
        return self.get_absolute_url()
    