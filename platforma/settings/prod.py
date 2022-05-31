from .base import * 
from decouple import config
import django_on_heroku
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['pythonplatformkz.herokuapp.com']


#S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
AWS_S3_OBJECT_PARAMETERS = {
    'CachControl': 'max-age=86400',
}
AWS_LOCATION = 'static'
AWS_QUERYSTRING_AUTH = False
AWS_HEADERS = {
    'Access-Control-Allow-Origin': '*'
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'mysite/static'),
]
STATIC_URL = f'http://{AWS_S3_CUSTOM_DOMAIN}/static/'

MEDIA_URL = f'http://{AWS_S3_CUSTOM_DOMAIN}/media/'

# heroku logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',

            # 'format': '[%(asctime)s]{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'datefmt': '%d/%b/%Y %H:%M:%S',
        },
        'simple': {
            'format': '{levelname} {message}',

        },
    },
   
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'MYAPP': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}
DEBUG_PROPAGATE_EXCEPTIONS = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'pythonplatformkz@gmail.com'
EMAIL_HOST_PASSWORD = 'platformadmin123'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False


# heroku

django_on_heroku.settings(locals())
del DATABASES['default']['OPTIONS']['sslmode']