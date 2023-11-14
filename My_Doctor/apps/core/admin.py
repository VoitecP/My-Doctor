from django.contrib import admin
from django.contrib.admin import  ModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import *

# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType


class UserAdmin(BaseUserAdmin):
    search_fields = ('first_name','last_name', 'username')
    search_help_text = 'Searching by: first name, last name, username'
    ordering = ('first_name','last_name', 'username')
    list_display = ('username', 'first_name', 'last_name', 'usertype')
    fieldsets = (
        ('User Info', {'fields': ('username', 'password', 'usertype')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', 
            {'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {'classes': ('wide',),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'password1',
                    'password2',
                    'usertype',
                ),
            },
        ),
    )




class PatientAdmin(admin.ModelAdmin):
    pass
    
    
class DoctorAdmin(admin.ModelAdmin):
    pass 

class DirectorAdmin(admin.ModelAdmin):
    pass 

class CategoryAdmin(admin.ModelAdmin):
    pass 

class VisitAdmin(admin.ModelAdmin):
    pass 

class PatientImageAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Visit, VisitAdmin)
admin.site.register(VisitImageFile, PatientImageAdmin)

####
 
# patient_group, created = Group.objects.get_or_create(name ='Patient Group')
# doctor_group, created = Group.objects.get_or_create(name ='Doctor Group')


# patient_content = ContentType.objects.get_for_model(Patient)
# permission = Permission.objects.create(codename ='patient_permission22', name ='Patient Permission22', content_type = patient_content)
# # permission += Permission.objects.create(codename ='patient2_permission',name ='Patient2 Permission', content_type = patient_content)
# patient_group.permissions.add(permission)


