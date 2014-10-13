# -*- coding: utf-8 -*-
# Django settings for akenergo_project project.
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)

import os

# _ = lambda s: s
PROJECTS_PATH = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'o#_pm6%2br@!$f9^ajq9n$9nutj1o$40nl-*4i43!rgc+v6q3s'


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['192.168.1.189', '127.0.0.1', 'localhost', '.akenergosnab.kz', '85.29.144.210']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    #'django.contrib.humanize',

    'energosite',
    'registration',
    'mptt',
    'captcha',
    'ckeditor',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'akenergo_project.urls'
WSGI_APPLICATION = 'akenergo_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'energosite', # Or path to database file if using sqlite3.
        'USER': 'energosite', # Not used with sqlite3.
        'PASSWORD': '11111111', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Asia/Tashkent'
LANGUAGES = (
    #    ('en', _('English')),
    (u'ru', u'RU'),
    (u'kk', u'KZ'),
)
SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECTS_PATH, "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECTS_PATH, "static")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# # List of finder classes that know how to find static files in
# # various locations.
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
# )
#
#
# # List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     #     'django.template.loaders.eggs.Loader',
# )


TEMPLATE_DIRS = (
    os.path.join(PROJECTS_PATH, "energosite", "templates"),
    # os.path.join(PROJECTS_PATH, "energosite", "templatetags"),
)


from django.conf import global_settings
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
     'django.core.context_processors.request',
)


# AUTH_PROFILE_MODULE = 'energosite.UserProfile'
ACCOUNT_ACTIVATION_DAYS = 2 # кол-во дней для хранения кода активации

AUTHENTICATION_BACKENDS = (
    'energosite.backends.PersonAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# для отправки кода активации
#AUTH_USER_EMAIL_UNIQUE = True
# EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST = 'localhost'
# EMAIL_PORT = 587
EMAIL_PORT = 2525
# EMAIL_HOST_USER = 'noreply@akenergosnab.kz'
# EMAIL_HOST_PASSWORD = '111111111111'
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'noreply@akenergosnab.kz'
DEFAULT_TO_EMAIL = ['support@akenergosnab.kz', 'ao1@akenergosnab.kz', 'ode1@akenergosnab.kz', 'orip1@akenergosnab.kz']
REGISTRATION_OPEN = True

MAX_ARTICLE_LENGTH = 35

GRAVATAR_SIZE = 80

# Загрузка базы
UPLOAD_DATA_PATH = '/opt/load_data/baza'
#UPLOAD_DATA_PATH = '/home/user/progs/convert_baza/baza'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'energosite_cache_table',
        'TIMEOUT': 21600,
    }
}

#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
#CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.word_challenge'
#CAPTCHA_DICTIONARY_MIN_LENGTH = 2
#CAPTCHA_DICTIONARY_MAX_LENGTH = 10
CAPTCHA_FONT_SIZE = 30
#CAPTCHA_FLITE_PATH = '/usr/bin/flite'

CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_JQUERY_URL = os.path.join(STATIC_URL, 'js/jquery-2.1.1.min.js')
