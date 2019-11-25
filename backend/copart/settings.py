"""
Django settings for copart project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from datetime import date
from collections import OrderedDict

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# PROJECT_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k(9t4(4b6fa)6*8vvsn+!m$+roxd$drz8+m3t4vj&1g2cp0uuk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#
ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ['*']

SITE_ID = 1


# Application definition

DJANGO_APPS = [
    'jet.dashboard',
    'jet',
    # 'modeltranslation',

    # Default Django apps:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Useful template tags:
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    # 'ckeditor',
    # 'rosetta',
    'constance',
    'constance.backends.database',
    # 'debug_toolbar',
    'imagekit',
    # 'silk',
    # 'django_celery_beat',
    # 'celerybeat_status',
]

LOCAL_APPS = [
    # custom users app
    'product',
    'product.templatetags.extra_filters',
    'clear_cache',
    # Your stuff: custom apps go here
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

COPART_ADMIN_URL = 'altes/'
LOGIN_URL = '/altes/login'

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'silk.middleware.SilkyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'copart.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'constance.context_processors.config',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'copart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'copart',
#         'USER': 'copart',
#         'PASSWORD': 'copart',
#         'HOST': 'db',
#         'PORT': '3306',
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'OPTIONS': {
#             'read_default_file': '/etc/mysql/mysql.conf.d/mysqld.cnf',
#         },
#     }
# }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold'],
            ['Link'],
            ['BulletedList', 'NumberedList']
        ]
    }
}

MODELTRANSLATION_TRANSLATION_FILES = ('product.translation',)
MODELTRANSLATION_TRANSLATION_REGISTRY = 'matau.translation'

CONSTANCE_CONFIG = OrderedDict([
    ('SCRAP_COPART_LOTS', (True, 'Scrap Copart Lots', bool)),
    ('SCRAP_COPART_INSERT_ONLY', (True, 'Scrap Copart INSERT', bool)),
    ('SCRAP_COPART_AUCTIONS', (True, 'Scrap Copart Auctions', bool)),
    ('REMOVE_NOT_EXIST_LOTS', (True, 'Remove not exist lots on copart', bool)),
    ('SCRAP_COPART_NOT_EXIST_LOTS', (True, 'Scrap Copart Not Exist Lots', bool)),
    ('SCRAP_IAAI_LOTS', (False, 'Scrap IAAI Lots', bool)),

    ('SHOW_SITES', (True, 'Show/Hide Sites', bool)),
    ('SHOW_SOLD', (True, 'Show/Hide Already Sold', bool)),
])

CONSTANCE_CONFIG_FIELDSETS = {
    'Scrap Settings': ('SCRAP_COPART_LOTS',
                       'SCRAP_COPART_INSERT_ONLY',
                       'SCRAP_COPART_AUCTIONS',
                       'REMOVE_NOT_EXIST_LOTS',
                       'SCRAP_COPART_NOT_EXIST_LOTS',
                       'SCRAP_IAAI_LOTS',
                       ),

    'Filter Settings': ('SHOW_SITES',
                        'SHOW_SOLD',
                        ),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

#
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CONSTANCE_DATABASE_CACHE_BACKEND = 'default'

CACHE_TTL = 60 * 60 * 24

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

ADMINS = (
    ("copart", "zazacopart1@gmail.com"),
)

MANAGERS = ADMINS

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'zazacopart1@gmail.com'
EMAIL_HOST_PASSWORD = 'm1llerh0u4e1'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = '[copart]'
SERVER_EMAIL = 'zazacopart1@gmail.com'
DEFAULT_FROM_EMAIL = 'zazacopart1@gmail.com'

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('zh-cn', gettext('China')),
)

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# settings for JET
JET_THEMES = [
    {
        'theme': 'default',
        'color': '#47bac1',
        'title': 'Default'
    },
    {
        'theme': 'green',
        'color': '#44b78b',
        'title': 'Green'
    },
    {
        'theme': 'light-green',
        'color': '#2faa60',
        'title': 'Light Green'
    },
    {
        'theme': 'light-violet',
        'color': '#a464c4',
        'title': 'Light Violet'
    },
    {
        'theme': 'light-blue',
        'color': '#5EADDE',
        'title': 'Light Blue'
    },
    {
        'theme': 'light-gray',
        'color': '#222',
        'title': 'Light Gray'
    }
]

JET_SIDE_MENU_COMPACT = True

# JET_INDEX_DASHBOARD = 'copart.dashboard.CustomIndexDashboard'

DATA_UPLOAD_MAX_NUMBER_FIELDS = 150000

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', ],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'ERROR',
            'propagate': True
        },
        'django.security.DisallowedHost': {
            'level': 'ERROR',
            'handlers': ['console', 'mail_admins', ],
            'propagate': True
        },
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}