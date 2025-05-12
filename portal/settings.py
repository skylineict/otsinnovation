from pathlib import Path
import os
from django.contrib import messages
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-71+^l)a+&h374x^j)64-+&s)w!ioijt1#v6^@7fz(8a(16a(q@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'userprofile',
    'dash',
    'courses',
    'cohorts',
    'ckeditor',
    'ckeditor_uploader',
    'projects',
    'homepage',
    'emailssending',
    'materials',
    'credential',
    'newdash',
    'studenttask',
    'facilitator',
    
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

ROOT_URLCONF = 'portal.urls'

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
                'cohorts.context_processors.get_cohorts',
                'cohorts.context_processors.get_profiles'
            ],
        },
    },
]

WSGI_APPLICATION = 'portal.wsgi.application'
CKEDITOR_UPLOAD_PATH = "uploads/"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'mydatas.qlite3',
    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'obidient',
#         'USER': 'obidient',
#         'PASSWORD': 'obidient',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/mediafiles/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')



STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'statics')
]


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MESSAGE_TAGS =    {
    
messages.DEBUG: 'alert-info',
messages.INFO:   'alert-info',
messages.SUCCESS: 'alert-success',
messages.WARNING: 'alert-warning',
messages.ERROR: 'alert-danger',
    
    
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'registration.MyUser' 

# LOGOUT_REDIRECT_URL = 'login'

#email settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
# EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=False)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# #email settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'  # Replace with your SMTP host
# EMAIL_PORT = 587  # Replace with your SMTP port
# EMAIL_USE_TLS = True  # Use TLS encryption for security
# EMAIL_HOST_USER = 'obidientsclass@gmail.com'  # Replace with your email address
# EMAIL_HOST_PASSWORD = 'fcyxanxbkwidvxro'  # Replace with your email password



CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False  # Set to True only if you're using HTTPS



CSRF_TRUSTED_ORIGINS = ['https://0907-105-113-10-208.ngrok-free.app']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0907-105-113-10-208.ngrok-free.app']



SESSION_COOKIE_DOMAIN = None
CSRF_COOKIE_DOMAIN = None

FLUTTERWAVE_HASH = config('FLUTTERWAVE_HASH')
FLUTTERWAVE_SECRET_KEY = config('FLUTTERWAVE_SECRET_KEY')
FLUTTERWAVE_PUBLIC_KEY = config('FLUTTERWAVE_PUBLIC_KEY')
FLUTTERWAVE_BASE_URL = config('FLUTTERWAVE_BASE_URL')