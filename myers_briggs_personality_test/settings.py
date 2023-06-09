"""
Django settings for myers_briggs_personality_test project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add /apps folder to python path
# https://stackoverflow.com/a/3948821
PROJECT_ROOT = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+b01b195k+y-+)0+7322%3!unm7x3h(a%0ydn@sn+-qud82r$j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    ALLOWED_HOSTS = ['*']
else:
    ALLOWED_HOSTS = ['example.com']

"""
Project Apps Definitions
Django Apps - Django Internal Apps
Third Party Apps before django - Apps installed via requirements.txt, which add before django apps
Third Party Apps after django - Apps installed via requirements.txt, which add after django apps
Project Apps - Project owned / created apps
Installed Apps = Django Apps + Third Part apps + Projects Apps
"""

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS_BEFORE = [
]

THIRD_PARTY_APPS_AFTER = [
]

PROJECT_APPS = [
    'personality_test'
]

INSTALLED_APPS = THIRD_PARTY_APPS_BEFORE + DJANGO_APPS + THIRD_PARTY_APPS_AFTER + PROJECT_APPS

"""
Middleware definitions
Django middleware - Django Internal middleware
Third Party middleware before django - Middleware installed via requirements.txt, which add before middleware
Third Party middleware after django - Middleware installed via requirements.txt, which add after middleware
"""

DJANGO_MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

THIRD_PARTY_MIDDLEWARE_BEFORE_DJANGO = [
    # 'corsheaders.middleware.CorsMiddleware',  # before ...CommonMiddleware
]

THIRD_PARTY_MIDDLEWARE_AFTER_DJANGO = [
]

MIDDLEWARE = THIRD_PARTY_MIDDLEWARE_BEFORE_DJANGO + DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE_AFTER_DJANGO

ROOT_URLCONF = 'myers_briggs_personality_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'myers_briggs_personality_test.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

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

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

# https://docs.djangoproject.com/en/4.1/ref/settings/#locale-paths
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

TIME_ZONE = 'Asia/Yekaterinburg'

USE_I18N = True

USE_TZ = True

# https://stackoverflow.com/a/70709867
USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Media files

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin URL Definition

ADMIN_URL = 'admin/'

# Logging configuration dictionary
# https://docs.djangoproject.com/en/4.1/ref/settings/#logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        '': {  # 'catch all' loggers by referencing it with the empty string
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# DATE settings

DATE_INPUT_FORMATS = ['%d.%m.%Y']
