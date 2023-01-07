from .settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-sdam(6erb76@!8f-0@w^o2n1j_b8c#ozstv7+ib+3cglqg&yap'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['192.168.1.125', 'localhost', '127.0.0.1', 'linux-vm']

X_FRAME_OPTIONS = 'SAMEORIGIN'

PORT = 8080

""" # Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = { 
	'default': { 
		'ENGINE': 'django.db.backends.postgresql', 
		'NAME': 'template', 
		'USER': 'postgres', 
		'PASSWORD': 'd3v3l0p3r', 
		'HOST': 'localhost', 
		'PORT': '5432' 
	} 
} 
 """

 # Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

