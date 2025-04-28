import os

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