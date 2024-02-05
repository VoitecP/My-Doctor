from . import board_urls, visit_urls
from django.urls import path, include

from ..urls import (  
    category_urls, 
    #patient_urls, 
    # doctor_urls,director_urls, 
    # category_urls, visit_urls,
    # summary_urls, file_urls, 
    )

app_name='apps.core'

urlpatterns = [
    path('user/', include(visit_urls)),
    # path('patient/', include(patient_urls)),
    # path('doctor/', include(doctor_urls)),
    # path('director/', include(director_urls)),
    path('category/', include(category_urls)),
    path('', include(board_urls)),
    # path('visit/', include(visit_urls)),
    # path('summary/', include(summary_urls)),
    # path('file/', include(file_urls)),
    ]



