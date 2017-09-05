from .common import *

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/hasker-messages'
EMAIL_HOST_USER = 'hasker@email.com'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

STATIC_URL = '/static/'

STATIC_ROOT = '/var/www/hasker/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = '/var/www/hasker/media/'
