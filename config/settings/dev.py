from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-ki8y=tc=$e4f_hz2+rjv_q=bdj&j37-fys$_(qz05tik)^6f='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    }
}

MEDIA_ROOT = 'qa/media'

if DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        INSTALLED_APPS.append('debug_toolbar')
        MIDDLEWARE.insert(
            MIDDLEWARE.index('django.middleware.common.CommonMiddleware') + 1,
            'debug_toolbar.middleware.DebugToolbarMiddleware'
        )


QUESTIONS_PER_PAGE = 5

ANSWERS_PER_PAGE = 2
