"""
Django settings for glasljudstva project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = dict(
    SECRET_KEY=os.getenv(
        "DJANGO_SECRET_KEY", "r^&^$8c*g$6db1s!s7uk9c!v%*ps)_0)h$!f3m7$%(o4b+5qwk"
    ),
    DEBUG=os.getenv("DJANGO_DEBUG", False),
    DATABASE_HOST=os.getenv("DJANGO_DATABASE_HOST", "localhost"),
    DATABASE_PORT=os.getenv("DJANGO_DATABASE_PORT", "5432"),
    DATABASE_NAME=os.getenv("DJANGO_DATABASE_NAME", "glasljudstva"),
    DATABASE_USER=os.getenv("DJANGO_DATABASE_USERNAME", "postgres"),
    DATABASE_PASSWORD=os.getenv("DJANGO_DATABASE_PASSWORD", "postgres"),
    STATIC_ROOT=os.getenv("DJANGO_STATIC_ROOT", os.path.join(BASE_DIR, "../static")),
    STATIC_URL=os.getenv("DJANGO_STATIC_URL_BASE", "/static/"),
    MEDIA_ROOT=os.getenv("DJANGO_MEDIA_ROOT", "/media/"),
    MEDIA_URL=os.getenv("DJANGO_MEDIA_URL_BASE", "/media/"),
)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env["SECRET_KEY"]
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env["DEBUG"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "HOST": env["DATABASE_HOST"],
        "PORT": env["DATABASE_PORT"],
        "NAME": env["DATABASE_NAME"],
        "USER": env["DATABASE_USER"],
        "PASSWORD": env["DATABASE_PASSWORD"],
    }
}

ALLOWED_HOSTS = ["localhost", "glas-ljudstva.si", "www.glas-ljudstva.si"]
CSRF_TRUSTED_ORIGINS = ["https://*.glas-ljudstva.si"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "rest_framework",
    "corsheaders",
    "django_comments",
    "zahteve",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "glasljudstva.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
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

WSGI_APPLICATION = "glasljudstva.wsgi.application"


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "glas-ljudstva",
    }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = env["STATIC_ROOT"]
STATIC_URL = env["STATIC_URL"]

MEDIA_ROOT = env["MEDIA_ROOT"]
MEDIA_URL = env["MEDIA_URL"]

# DJANGO STORAGE SETTINGS
if os.getenv("DJANGO_ENABLE_S3", False):
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3StaticStorage"
    AWS_ACCESS_KEY_ID = os.getenv("DJANGO_AWS_ACCESS_KEY_ID", "<TODO>")
    AWS_SECRET_ACCESS_KEY = os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY", "<TODO>")
    AWS_STORAGE_BUCKET_NAME = os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME", "djnd")
    AWS_DEFAULT_ACL = (
        "public-read"  # if files are not public they won't show up for end users
    )
    AWS_QUERYSTRING_AUTH = (
        False  # query strings expire and don't play nice with the cache
    )
    AWS_LOCATION = os.getenv("DJANGO_AWS_LOCATION", "glas-ljudstva")
    AWS_S3_REGION_NAME = os.getenv("DJANGO_AWS_REGION_NAME", "fr-par")
    AWS_S3_ENDPOINT_URL = os.getenv(
        "DJANGO_AWS_S3_ENDPOINT_URL", "https://s3.fr-par.scw.cloud"
    )
    AWS_S3_SIGNATURE_VERSION = os.getenv("DJANGO_AWS_S3_SIGNATURE_VERSION", "s3v4")

# CORS
CORS_ALLOW_ALL_ORIGINS = True
LOGIN_REDIRECT_URL = "/"

SITE_ID = 1

if os.getenv("APP_ENV", "development") == "production":
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.getenv("EMAIL_HOST", "")
    EMAIL_PORT = os.getenv("EMAIL_PORT", "")
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_SSL = True
    FROM_EMAIL = os.getenv("FROM_EMAIL", "dummy@email.com")

else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    FROM_EMAIL = "dummy@email.com"

FRONT_URL = os.getenv("FRONT_URL", "http://localhost:8000/")

LOGIN_URL = "/login/"
