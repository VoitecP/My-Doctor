"""
Django settings for My_Doctor project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os, sys

from pathlib import Path

from decouple import config


# Add for specific apps path
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Add user-files
MEDIA_ROOT = os.path.join(BASE_DIR, 'user-files')


# URL used to access files
MEDIA_URL = 'user-files/'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG')

ALLOWED_HOSTS = [config('ALLOWED_HOST_1'),
                 config('ALLOWED_HOST_2'),
                 config('ALLOWED_HOST_3')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    ##  Packages
    'rest_framework',
    'rest_framework.authtoken',
    'drf_spectacular',


    ## Removed
    # 'dj_rest_auth',  
    # 'dj_rest_auth.registration',
    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',

    ##  Local Apps
    'apps.core',
    'apps.api',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'My_Doctor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'My_Doctor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

POSTGRES_DB = config('POSTGRES_DB')

if POSTGRES_DB == True:
    DATABASES = {
        "default": {
            "ENGINE": config('POSTGRES_ENGINE'),
            "NAME": config('POSTGRES_DATABASE'),
            "USER": config('POSTGRES_USER'),
            "PASSWORD": config('POSTGRES_PASSWORD'),
            "HOST": config('POSTGRES_HOST'),
            "PORT": config('POSTGRES_PORT'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LOGIN_REDIRECT_URL = '/'

LOGIN_URL = 'login/'

LOGOUT_REDIRECT_URL = '/'



# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Default Time zone
# TIME_ZONE = 'UTC'

TIME_ZONE = "Europe/Warsaw"

USE_I18N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/



# Pythoneverywhere settings

# python manage.py collectstatic
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


STATIC_URL = '/static/'

# Disable it when using  command:  python manage.py collectstatic 
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'core.User'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': [
    #                     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny",],  

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
        "rest_framework.permissions.IsAuthenticated",
        ], 

    
    'DEFAULT_AUTHENTICATION_CLASSES': [
        ## Correct order for authentication
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
         ## Disabled
        # 'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ],




    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 4,

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    
}


SPECTACULAR_SETTINGS = {
    'TITLE': 'My Doctor',
    'DESCRIPTION': 'My Doctor API Documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Other Settings
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "displayRequestDuration": True,
    },
}

# If error in when registering new user in endpoint (api/dj-rest-auth/register/') 
# # Use this setting
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


REST_AUTH = {
 
}

####
### Disabled
####


# REST_USE_JWT = True

# JWT_AUTH_COOKIE = 'my-app-auth'


# AUTHENTICATION_BACKENDS = [
#     'allauth.account.auth_backends.AuthenticationBackend',
#     'django.contrib.auth.backends.ModelBackend',
# ]


# ACCOUNT_AUTHENTICATION_METHOD = 'username'
# ACCOUNT_EMAIL_REQUIRED = False
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# ACCOUNT_CONFIRM_EMAIL_ON_GET = True
# LOGIN_URL = 'http://localhost:8000/users/login'


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'email@gmail.com'
# EMAIL_HOST_PASSWORD = ********
# EMAIL_PORT = 587

