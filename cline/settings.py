#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

"""
Django settings for cline project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-1s@$2#65&=!vudidrlw%x!dzy$1wy@0(o-9dl_)@sen94*f^6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cline',
    'ivr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'cline.urls'

WSGI_APPLICATION = 'cline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            # 'class': 'django.utils.log.AdminEmailHandler',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'iso8601': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# True to serve files via django server, False to let Nginx do it
SERVE_AUDIO_FILES = True

ORANGE = 'orange'
MALITEL = 'malitel'
FOREIGN = 'foreign'
OPERATORS = {ORANGE: ("Orange MALI", [7, 9, 4, 8, 90, 91]),
             MALITEL: ("Malitel", [2, 6, 98, 99]),
             FOREIGN: ("Extérieur", [])}
COUNTRY_PREFIX = 223
IVR_VOICE = 'renaud'
# IVR_VOICE = 'kani'

VOICE_POP3_SERVER = '192.168.5.65'
VOICE_POP3_PORT = 110
VOICE_POP3_USER = 'reg'
VOICE_POP3_PASSWD = 'reg'
VOICE_POP3_POLL_INTERVAL = 5 # seconds
VOICE_POP3_DOMAIN = "voiceblue.ylm"
VOICE_POP3_EMAIL_ADDRESS = "{user}@{domain}".format(user=VOICE_POP3_USER,
                                                    domain=VOICE_POP3_DOMAIN)

VOICE_AGREEMENT_MESSAGE = ("Merci d'avoir enregistré votre rapport. "
                           "Nous autorisez-vous à vous rappeller pour obtenir "
                           "plus d'informations ? Si oui, répondez OUI.")

SYNCHRO_URL = "user@server.local:repo/"

# Persons getting notified of new reports
CONTACT_NUMBERS = []
CONTACT_EMAILS = []
ONLINE_URL = "http://my.web.site"
NOTIFICATION_MESSAGE = ("A new *{type}* report has been received on the "
                        "Anti-corruption Hotline from {identity}. {url}")

EMAIL_USE_TLS = False
EMAIL_HOST = VOICE_POP3_SERVER
EMAIL_PORT = 25
EMAIL_HOST_USER = VOICE_POP3_USER
EMAIL_HOST_PASSWORD = VOICE_POP3_PASSWD

try:
    from cline.settings_local import *
except ImportError:
    pass

