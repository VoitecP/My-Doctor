from django.contrib import admin
from .models import *
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    # list_display = ("name","surname",)
    pass
    
    # readonly_fields=('slug',)
   
    
class DoctorAdmin(admin.ModelAdmin):
   
    # prepopulated_fields={'slug':('name','surname')}
    # readonly_fields=('slug',)
    pass 




# class Patient


##############

class UserAdmin(admin.ModelAdmin):
    # list_display = ("name","surname",)
    # prepopulated_fields={'slug':('name','surname')}
    # readonly_fields=('slug',)
    pass
    # search_fields = ("last_name",)
    # search_help_text = "User last name"
    
    


   
    

admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)


# admin.site.register(User)
# admin.site.register(Patient)
# admin.site.register(Doctor)