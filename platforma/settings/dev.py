from .base import * 
import os

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!pxaor%gc8e96py^og((3lza_0r9wx(#_h*zlmad&jaee4v8-2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pythonplatformkz@gmail.com'
EMAIL_HOST_PASSWORD = 'platformadmin123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/') 

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 
