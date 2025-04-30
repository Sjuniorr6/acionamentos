from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification
from django.contrib.contenttypes.models import ContentType
from formacompanhamento.models import OcorrenciaTransporte

def get_user(recipient_id):
    User = get_user_model()
    return User.objects.get(id=recipient_id)

@shared_task
def create_notification(recipient_id, title, message, ocorrencia_id=None):
    recipient = get_user(recipient_id)
    notification_kwargs = {
        'recipient': recipient,
        'title': title,
        'message': message,
    }
    if ocorrencia_id:
        ocorrencia = OcorrenciaTransporte.objects.get(id=ocorrencia_id)
        notification_kwargs['content_object'] = ocorrencia
    Notification.objects.create(**notification_kwargs) 