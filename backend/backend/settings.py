"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import dotenv as env 
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'dotenv', '.env')
load_dotenv(dotenv_path)

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]


CACHE_TTL = 60 * 15

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_URL =  "http://localhost:8000"
HOST_BACKEND_URL = "https://joshua-trefzer.developerakademie.org"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zv*r+2ol!&m#cd8g9^@_rqnang&p9&=rfmfnp6@f6l8z_&zv5c"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "joshua-trefzer.developerakademie.org",
    "https://joshua-trefzer.developerakademie.org",
    "https://videoflix.joshuatrefzer.de" ,
    "videoflix.joshuatrefzer.de",
]

CLIENT_BASE_URL = "https://videoflix.joshuatrefzer.de" 

CORS_ALLOWED_HOSTS = [
    "localhost",
    "joshua-trefzer.developerakademie.org",
    "https://videoflix.joshuatrefzer.de" ,
    "videoflix.joshuatrefzer.de",
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",
    "https://localhost",
    "https://videoflix.joshuatrefzer.de" ,
]



EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.getenv("DEVMAIL")
EMAIL_HOST_USER = os.getenv("DEVMAIL")
EMAIL_HOST_PASSWORD = os.getenv("DEVPW")


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "videoflix",
    }
}

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "users",
    "videos.apps.VideosConfig",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "debug_toolbar",
    "django_rq",
    "import_export",
    "django_rest_passwordreset",
]

REST_FRAMEWORK = {
    
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

AUTH_USER_MODEL = "users.CustomUser"

AUTHENTICATION_BACKENDS = ["users.backends.EmailBackend"]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


RQ_QUEUES = {
    "default": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0,
        "DEFAULT_TIMEOUT": 360,
    },
}


MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"



ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"



DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "videoflix",
        "USER": "myuser",
        "PASSWORD": "auschoj34",
        "HOST": "localhost",
        "PORT": "5432",
    }
}


CSRF_TRUSTED_ORIGINS = [
    "https://joshua-trefzer.developerakademie.org",
]


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

STATIC_ROOT = os.path.join(BASE_DIR, "static/staticfiles")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
