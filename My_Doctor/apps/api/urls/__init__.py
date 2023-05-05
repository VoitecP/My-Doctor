from django.urls import path, include

from ..urls import (
                    urls_views,
                    urls_generic,
                    urls_viewsets,
)

# app_name='apps.api'
app_name='api'

# urlpatterns = [
#     path('views/', include(urls_views)),
#     path('generic/', include(urls_generic)),
#     path('viewsets/', include(urls_viewsets)),
# ]


urlpatterns = [
    path('', include(urls_views)),
    path('', include(urls_generic)),
    path('', include(urls_viewsets)),
]



