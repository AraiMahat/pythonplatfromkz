"""
Django settings for platforma project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

from django import conf
from decouple import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

SECRET_KEY = '%20!5gxdyuu!mxtk^#d2olcvt(^h3q1&u8_fgh4%n!%a5f&@ih'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.vercel.app']
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

import dj_database_url

from dotenv import load_dotenv, find_dotenv



LOGIN_REDIRECT_URL = '/topics'
LOGIN_URL = '/login'
LOGOUT_REDIRECT_URL = '/'

CKEDITOR_UPLOAD_PATH = 'uploads/'
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'widget_tweaks',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'platforma',
    'universystem',
    'ckeditor',
    'ckeditor_uploader',
    'django_extensions',
    'storages',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'platforma.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'platforma.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

load_dotenv(find_dotenv())

DATABASES = {
        
    'default':  dj_database_url.config(default='sqlite:///db.sqlite3', conn_max_age=600)
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
  
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True







# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


# STATIC_ROOT = os.path.join(BASE_DIR, 'static') 


# MEDIA_ROOT = os.path.join(BASE_DIR, 'media') 

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')




# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

DEFAULT_AUTO_FIELD='django.db.models.AutoField' 

import dj_database_url
db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)



# MEDIAFILES_LOCATION = 'media'
# DEFAULT_FILE_STORAGE = 'Management.storage_backends.MediaStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'static'
# AWS_QUERYSTRING_AUTH = False
# AWS_HEADERS = {
#     'Access-Control-Allow-Origin': '*'
# }

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATIC_URL = 'http://pythonplatformkz.s3.amazonaws.com/static/'
# MEDIA_URL = 'http://pythonplatformkz.s3.amazonaws.com/media/'
STATIC_ROOT = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

