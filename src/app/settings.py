from os import getenv, makedirs, path
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

load_dotenv()

# ======================================================
# Основные настройки проекта
# ======================================================
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = getenv('SECRET_KEY', 'secret')
DEBUG = int(getenv('DEBUG', 0))
ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', '127.0.0.1, localhost').split(', ')
SITE_DOMAIN = getenv('SITE_DOMAIN', '')
SITE_BASE_URL = f'https://{SITE_DOMAIN}/'

# ======================================================
# Конфигурация CORS и CSRF
# ======================================================
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

CSRF_TRUSTED_ORIGINS = getenv('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000, http://localhost:8000').split(', ')

# ======================================================
# Установка приложений (Django, сторонние, локальные)
# ======================================================
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'django_celery_beat',
    'drf_yasg',
    'rest_framework',
    'rest_framework_api_key',
]
LOCAL_APPS = [
    'accounting',
    'bybit',
    'core',
    'users',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ======================================================
# Конфигурация middleware
# ======================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================================================
# URL и WSGI приложения
# ======================================================
ROOT_URLCONF = 'app.urls'
WSGI_APPLICATION = 'app.wsgi.application'

# ======================================================
# Конфигурация базы данных
# ======================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('POSTGRES_DB', str(BASE_DIR / 'db.sqlite3')),
        'USER': getenv('POSTGRES_USER', 'user'),
        'PASSWORD': getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': getenv('SQL_HOST', 'localhost'),
        'PORT': getenv('SQL_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SALT_KEY = getenv('SALT_KEY', 'salt-debug')

# ======================================================
# Пользователи
# ======================================================
AUTH_USER_MODEL = 'users.User'

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

# ======================================================
# Локализация и часовой пояс
# ======================================================
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================================================
# Конфигурация REST API и Swagger
# ======================================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'core.api.permissions.HasExternalServiceAPIKey',
    ]
}

SWAGGER_SETTINGS = {'SECURITY_DEFINITIONS': {'Api-Key': {'type': 'apiKey', 'name': 'Authorization', 'in': 'header'}}}
SWAGGER_USE_COMPAT_RENDERERS = False

# ======================================================
# Настройка статики и шаблонов
# ======================================================
STATIC_URL = 'static/'
STATIC_DIR = BASE_DIR / 'staticfiles'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR]

TEMPLATE_DIR = STATIC_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ======================================================
# Конфигурация Redis и Celery и Health Check
# ======================================================
REDIS_URL = getenv('REDIS_HOST', 'redis://127.0.0.1')
REDIS_PORT = int(getenv('REDIS_PORT', 6379))
REDIS_HOST = REDIS_URL.split('://')[1]

CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_BROKER_URL = REDIS_URL
CELERY_BACKEND_URL = REDIS_URL
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_RESULT_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = f'{REDIS_URL}/0'
CELERY_RESULT_EXPIRES = 60

BROKER_URL = f'{REDIS_URL}/0'
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

# ======================================================
# Логирование
# ======================================================
DATETIME_FORMATTER = '%d/%b/%Y %H:%M:%S'
LOG_FORMATTER = '[%(asctime)s] logger: %(name)s\nLevel - %(levelname)s, func - %(funcName)s\n%(message)s\n'
LOG_DIR = BASE_DIR / 'logs'
if not path.exists(LOG_DIR):
    makedirs(LOG_DIR)

LOGGING: dict[str, Any] = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'main': {
            'format': LOG_FORMATTER,
            'datefmt': DATETIME_FORMATTER,
        },
    },
    'handlers': {
        'console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'main',
        },
        'timed_rotating_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_DIR / 'main.log',
            'formatter': 'main',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
        'telegram': {
            'level': 'DEBUG',
            'class': 'app.logging_handlers.TelegramHandler',
            'formatter': 'main',
        },
        'celery_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': LOG_DIR / 'celery.log',
            'formatter': 'main',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'main': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'telegram': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

if not DEBUG:
    LOGGING['loggers']['django']['handlers'] = ['console', 'telegram', 'timed_rotating_file']
    LOGGING['loggers']['django']['level'] = 'ERROR'
    LOGGING['loggers']['celery']['handlers'] = ['console', 'celery_file']
    LOGGING['loggers']['celery']['level'] = 'INFO'
    LOGGING['loggers']['main']['handlers'] = ['console', 'timed_rotating_file']
    LOGGING['loggers']['telegram']['handlers'] = ['console', 'timed_rotating_file', 'telegram']
