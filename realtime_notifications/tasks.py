from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification

def get_user(recipient_id):
    User = get_user_model()
    return User.objects.get(id=recipient_id)

@shared_task
def create_notification(recipient_id, title, message):
    recipient = get_user(recipient_id)
    Notification.objects.create(
        recipient=recipient,
        title=title,
        message=message,
        content_type=None,
        object_id=None
    ) 