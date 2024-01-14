"""My_Doctor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include , re_path
from django.views.generic.base import RedirectView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
# from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
# from dj_rest_auth.views import (LoginView, LogoutView, 
#                                PasswordResetView, PasswordResetConfirmView)

from apps.api import urls
from apps.api.urls import viewsets_urls


static_files = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# app_name = 'core'
app_name='apps.core'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core API aplication
    path('api/', include(urls, namespace='base-api')),
    path('api-viewset/', include(viewsets_urls, namespace='viewset-api')),

    # DRF  Authentication
    path('api/rest-auth/', include('rest_framework.urls')),
    path('api/rest-auth/register/',RedirectView.as_view(pattern_name='apps.api:user-register'), name='user-register-base'),
    
    # Dj Rest Auth Views - removed
    # path('register/', RegisterView.as_view()),
    # path('auth/', include('dj_rest_auth.urls')),
    # path('register/', include('dj_rest_auth.registration.urls')),
    # path('login/', LoginView.as_view()),
    # path('logout/', LogoutView.as_view()),
    # path('password-reset/', PasswordResetView.as_view()),
    # path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),  
    # TODO ..
    ## Removed
    # path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('api/dj-rest-auth/register/', include('dj_rest_auth.registration.urls')),

    # Spectacular API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ##
    
] + static_files
