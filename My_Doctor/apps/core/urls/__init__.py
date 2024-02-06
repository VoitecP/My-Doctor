from . import base_urls, panel_director_urls, panel_doctor_urls, panel_patient_urls
from django.urls import path, include

from ..urls import (  
    category_urls, 

    base_urls,
    panel_patient_urls,
    #patient_urls, 
    # doctor_urls,director_urls, 
    # category_urls, visit_urls,
    # summary_urls, file_urls, 
    )

app_name='apps.core'

urlpatterns = [
    path('', include(base_urls)),


    path('patient/', include(panel_patient_urls)),
    # path('doctor/', include(doctor_urls)),
    # path('director/', include(director_urls)),
    path('category/', include(category_urls)),
    # path('visit/', include(visit_urls)),
    # path('summary/', include(summary_urls)),
    # path('file/', include(file_urls)),
    ]



