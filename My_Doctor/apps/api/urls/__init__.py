from django.urls import path, include

from ..urls import (  
    user_urls, patient_urls, doctor_urls,
    director_urls, category_urls, visit_urls,
    summary_urls, file_urls, viewsets_urls
    )


# app_name='api' 
app_name='apps.api'

urlpatterns = [
    
    path('user/', include(user_urls)),
    path('patient/', include(patient_urls)),
    path('doctor/', include(doctor_urls)),
    path('director/', include(director_urls)),
    path('category/', include(category_urls)),
    path('visit/', include(visit_urls)),
    path('summary/', include(summary_urls)),
    path('file/', include(file_urls)),
    ]



