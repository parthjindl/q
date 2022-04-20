"""
Django settings for greenCan project.

Generated by 'django-admin startproject' using Django 4.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import django_heroku
import environ
import sys
import os
from django.urls import reverse_lazy

# CONFIGS
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.environ.get("DEBUG", True))
ALLOWED_HOSTS = [
    "127.0.0.1",
    "greencan.herokuapp.com",
    "greencan-dev.herokuapp.com",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django.contrib.sites",
    "home",
    "accounts",
    "reuse",
    "recycle",
    "reduce",
    "rewards",
    "notification",
    "helper",
    "moderation",
    "crispy_forms",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "greenCan.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", BASE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "greenCan.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME", ""),
        "USER": os.environ.get("DATABASE_USER", ""),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("DATABASE_HOST", ""),
        "PORT": "5432",
        "TEST": {"NAME": os.environ.get("TEST_DATABASE_NAME", "")},
    }
}


if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("TEST_DATABASE_NAME", ""),
        "USER": os.environ.get("TEST_DATABASE_USER", ""),
        "PASSWORD": os.environ.get("TEST_DATABASE_PASSWORD", ""),
        "HOST": os.environ.get("TEST_DATABASE_HOST", ""),
        "PORT": "5432",
        "TEST": {"NAME": os.environ.get("TEST_DATABASE_NAME")},
    }


FIRE_BASE_CONFIG = {
    "apiKey": f"{os.environ.get('FIRE_STORAGE_API_KEY')}",
    "authDomain": "greencan-tandon.firebaseapp.com",
    "projectId": "greencan-tandon",
    "databaseURL": "https://greencan-tandon-default-rtdb.firebaseio.com/",
    "storageBucket": "greencan-tandon.appspot.com",
    "messagingSenderId": f"{os.environ.get('FIRE_MESSAGE_SENDER_ID')}",
    "appId": f"1:{os.environ.get('FIRE_MESSAGE_SENDER_ID')}:web:{os.environ.get('FIRE_APP_ID')}",
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/New_York"

USE_I18N = True

USE_TZ = True

SECURE_BROWSER_XSS_FILTER = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static/"]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

LOGIN_URL = reverse_lazy("accounts:login")

LOGOUT_REDIRECT_URL = LOGIN_URL

LOGIN_REDIRECT_URL = reverse_lazy("home:index")  # change this to your home page

# email configuration for development
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# email configuration in production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_USE_TLS = True

EMAIL_HOST = "smtp.gmail.com"

EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")

EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_PORT = 587

FIREBASE_HOST_USER = EMAIL_HOST_USER

FIREBASE_HOST_PASSWORD = EMAIL_HOST_PASSWORD

# Time in seconds after each login attempt
LOGIN_ATTEMPTS_TIME_LIMIT = 0
# limit the amount of attempts to which the user will be inactive and password set mail sent
MAX_LOGIN_ATTEMPTS = 5

ACCOUNT_ACTIVATION_DAYS = 7

CRISPY_TEMPLATE_PACK = "bootstrap4"

SITE_ID = 2

# Additional configuration settings

ACCOUNT_USER_MODEL_USERNAME_FIELD = None

ACCOUNT_EMAIL_REQUIRED = True

ACCOUNT_USERNAME_REQUIRED = False

ACCOUNT_AUTHENTICATION_METHOD = "email"

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False
# Attempt to bypass the signup form by using fields (e.g. username, email)
SOCIALACCOUNT_AUTO_SIGNUP = True

SOCIALACCOUNT_LOGIN_ON_GET = True  # bypass the "do you want to login page"

# add max Gauth login attempts
# ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5

SOCIALACCOUNT_PROVIDERS = {
    "google": {"SCOPE": ["profile", "email"], "AUTH_PARAMS": {"access_type": "online"}}
}

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # authenticate using django
    "allauth.account.auth_backends.AuthenticationBackend",
]
SOCIAL_AUTH_URL_NAMESPACE = "social"
django_heroku.settings(locals(), test_runner=False)
