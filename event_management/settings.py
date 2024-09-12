"""
Django settings for event_management project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-he3l!2bpuotrrccv(&kg*h)lytlti6slt7o%(py5cad-d_1l$n"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Original
ALLOWED_HOSTS = []
# DEBUG = False settings, see https://docs.djangoproject.com/en/4.2/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = [".localhost", "127.0.0.1", "[::1]"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "django_bootstrap5",
    "events",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # DebugToolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "event_management.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "event_management.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "mariadb": {
        # https://docs.djangoproject.com/en/4.2/ref/databases/#mysql-notes
        # pip install mysqlclient
        "ENGINE": "django.db.backends.mysql",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "NAME": "events",
        "USER": "django",
        "PASSWORD": "django",
    },
    "postgresql": {
        # https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes
        # https://www.psycopg.org/psycopg3/docs/basic/install.html
        # pip install "psycopg[binary]"
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "127.0.0.1",
        "PORT": "5432",
        "NAME": "events",
        "USER": "django",
        "PASSWORD": "django",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Manually added

# Bootstrap theme
BOOTSTRAP5 = {
    "theme_url": "/static/main.css",
}

# DebugToolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

# For LoginView / LoginRequiredMixin
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "/"

EVENTS = {
    # Appears at the top of the website and in email subjects
    "TITLE": "Django Events",
    # Appears at the contact/support page
    "ADMINISTRATOR_NAME": "Devola Teamson",
    "ADMINISTRATOR_EMAIL": "devola.teamson@example.org",
    # Disable working time events (if only leisure events are enabled, no supervisors or moderators required)
    "ONLY_LEISURE": False,
}