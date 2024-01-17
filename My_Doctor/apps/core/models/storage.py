import os
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator

def polish_chars(name):
    '''
    Polish char replace
    # TODO
    '''
    dict = {'ą': 'a', 
            'ę': 'e', 
            'ć': 'c', 
            'ł': 'l', 
            'ń': 'n', 
            'ó': 'o', 
            'ś': 's', 
            'ź': 'z', 
            'ż': 'z'}

    for old, new in dict.items():
        name = name.replace(old, new)

    return name


def make_thumb(self):
    height=200
    #width=200
   
    image=self.image
    image_h=self.image.height
    image_w=self.image.width
    thumb=self.thumb
    
    ratio=image_w/image_h
    width=int(round(height * ratio))

    try:
        img = Image.open(image)
        img.thumbnail((height,width), Image.LANCZOS)
        img_name, img_ext =os.path.splitext(image.name)
        img_ext.lower()

        if img_ext == '.jpg' or '.jpeg':     
            FTYPE = 'JPEG'
        elif img_ext == '.png':
            FTYPE = 'PNG'

        thumb_name = f'{img_name}_thumb{height}x{width}{img_ext}'
        temp_thumb = BytesIO()              # SavE thumbnail to in-memory file as StringIO
        img.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        thumb.save(thumb_name, ContentFile(temp_thumb.read()), save=False) # set save must be False !
        temp_thumb.close()
    except IOError:
        pass
    

def user_image_path(instance, filename):
    user = getattr(instance, 'user', None)
    user_id = getattr(user, 'id', 'None')
    return f'user_{user_id}/images/{filename}'

def user_thumb_path(instance, filename):
    user = getattr(instance, 'user', None)
    user_id = getattr(user, 'id', 'None')
    return f'user_{user_id}/thumbs/{filename}'

def ext_validator(self):
    validator=FileExtensionValidator(allowed_extensions=['jpg','png'])
    return validator


