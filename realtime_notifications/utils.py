from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

def send_notification(user, title, message):
    # Criar a notificação no banco de dados
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message
    )

    # Enviar a notificação via WebSocket para todos os usuários conectados
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_all",  # Grupo global para todos os usuários
        {
            "type": "notification_message",
            "message": {
                "id": notification.id,
                "title": title,
                "message": message,
                "created_at": notification.created_at.isoformat()
            }
        }
    )
    
    return notification 