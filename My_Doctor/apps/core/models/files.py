import uuid
from django.db import models
from django.utils.crypto import get_random_string as rnd


from apps.core import storage

from ..models import Visit, User



class ImageFile(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    # user = models.ForeignKey(User, models.PROTECT, null=True, blank=True, default=None)
    image=models.ImageField(upload_to=storage.user_image_path, 
                            validators=[storage.ext_validator], blank=False)
    thumb=models.ImageField(upload_to=storage.user_thumb_path, blank=True, editable=True)
    # title=models.CharField(max_length=50, blank=False, default=None)
            
    class Meta:
        abstract=True

   
    def save(self, *args, **kwargs):
        storage.make_thumb(self)
        super().save(*args, **kwargs)

    @property
    def image_url(self):
        return self.image.url
    
    @property
    def thumb_url(self):
        return self.thumb.url
    

class VisitImageFile(ImageFile):
    
    visit = models.ForeignKey(Visit,models.CASCADE, related_name='visit_images', null=True, blank=True, default=None)
    
    