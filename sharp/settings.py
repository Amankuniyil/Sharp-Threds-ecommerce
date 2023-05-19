"""
Django settings for sharp project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=@a!*8ydb4xn(z2u0npg9$56-!2h(f&q_6gc=cen#oz8s70d&@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ['sharpthreads.store']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'adminpanel',
    'accounts',
    'crispy_forms',
    'crispy_bootstrap5',
    'category',
    'main',
    'carts',
    'orders',
    'user',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'sharp.middleware.AuthMiddleware',

    
]

ROOT_URLCONF = 'sharp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'category.context_processors.category_links',
                'category.context_processors.sub_category_links',
                'main.context_processors.latest_products1',
                'main.context_processors.latest_products2',
                'main.context_processors.offer_products1',
                'main.context_processors.offer_products2',
                'main.context_processors.selling_products1',
                'main.context_processors.selling_products2',
                'carts.context_processors.counter',
                'carts.context_processors.total',
            ],
        },
    },
]

WSGI_APPLICATION = 'sharp.wsgi.application'

AUTH_USER_MODEL = 'accounts.Account'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sharp',
        'USER': 'aman',
        'PASSWORD': 'aman123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

#STATIC_ROOT = BASE_DIR / "staticfiles"



STATIC_ROOT = '/home/ubuntu/Sharp-Threds-ecommerce/staticfiles'

STATIC_FILES = ['/home/ubuntu/Sharp-Threds-ecommerce/static']


CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR/'media'





OTP_SECRET=''

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_HOST_USER='pdjango55@gmail.com'
EMAIL_HOST_PASSWORD='ormjnxvahdfvrfrg'
EMAIL_USE_TLS=True


MEDIA_ROOT = os.path.join(BASE_DIR,"media")
MEDIA_URL = "/media/"

RAZORPAY_ID = 'rzp_test_bSa79V3eWORvIC'
RAZORPAY_KEY = 'iC9KUbEVMQ8IGOswXKD9OGCz'