from django.apps import AppConfig


class RealtimeNotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'realtime_notifications'

    def ready(self):
        import realtime_notifications.signals
