import os
from datetime import datetime
import pytz

# Configurações de fuso horário
TIME_ZONE = 'America/Sao_Paulo'
USE_TZ = True

# Configuração para usar o fuso horário local para entrada de dados
USE_L10N = True
USE_I18N = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'formacompanhamento': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    'core',
    'formacompanhamento',
    'realtime_notifications',
    'notifications',  # Django notifications
]

# Cache local simples
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Configurações básicas de notificação
NOTIFICATIONS_CONFIG = {
    'SOFT_DELETE': True,
    'MARK_AS_READ_AJAX': True,  # Habilita marcação como lida via AJAX
    'REFRESH_INTERVAL': 120000,  # 120 segundos em milissegundos
} 