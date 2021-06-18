"""
Django settings for simple_cms project.

Generated by 'django-admin startproject' using Django 3.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import json

from dotenv import dotenv_values
from pathlib import Path


config =  dotenv_values('.env')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('SECRET_KEY', '123xyz')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = eval(config.get('DEBUG', 'True'))

ALLOWED_HOSTS = json.loads(config.get('ALLOWED_HOSTS', '[]'))


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    #
    'django_filters',
    'oauth2_provider',
    'rest_framework',

    #
    'simple_cms_admin',
    'simple_cms_admin_tenant',

    #
    'simple_cms_api',
    'simple_cms_api_tenants',

    #
    'simple_cms_frontend',
    'simple_cms_frontend_homepage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simple_cms.urls'

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

WSGI_APPLICATION = 'simple_cms.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_VALIDATION_ROOT = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': f'{AUTH_VALIDATION_ROOT}.UserAttributeSimilarityValidator'},
    {'NAME': f'{AUTH_VALIDATION_ROOT}.MinimumLengthValidator'},
    {'NAME': f'{AUTH_VALIDATION_ROOT}.CommonPasswordValidator'},
    {'NAME': f'{AUTH_VALIDATION_ROOT}.NumericPasswordValidator'},
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#

OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope',
        'write': 'Write scope',
        'groups': 'Access to your groups'
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'simple_cms_api.pagination.ResultPagination',
    'PAGE_SIZE': 10
}

AUTH_USER_MODEL = 'simple_cms_api.User'

THING_MODEL = 'simple_cms_api.Thing'  # ???? delete?


# API

SIMPLE_CMS_API_THING_CLASSES = [
    'simple_cms_api_tenants.things.TenantThing'
]


# ADMIN

API_URL = 'http://localhost:8000'
API_SECURE_THINGS_ENDPOINT = '/secure-api/things/'

SIMPLE_CMS_ADMIN_THING_CLASSES = [
    'simple_cms_admin_tenant.things.TenantThing'
]

PROJECT_TITLE = 'SIMPLE CMS'

DEFAULT_CONTENT_LANGUAGE = ['en', 'English']
CONTENT_LANGUAGE_CHOICES = [
    DEFAULT_CONTENT_LANGUAGE,
    ['ga', 'Gaeilge']
]


# FRONTEND

SIMPLE_CMS_FRONTEND_THING_CLASSES = [
    'simple_cms_frontend_homepage.things.HomepageThing',
    'simple_cms_frontend_homepage.things.HomepageNoLanguageThing',
]
