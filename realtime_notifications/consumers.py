import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Notification

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            self.user_group_name = f"user_{self.scope['user'].id}"
            
            # Adicionar ao grupo do usuário
            await self.channel_layer.group_add(
                self.user_group_name,
                self.channel_name
            )
            
            await self.accept()
            
            # Enviar contagem inicial
            count = await self.get_unread_count()
            await self.send(text_data=json.dumps({
                'type': 'notification_message',
                'count': count
            }))

    async def disconnect(self, close_code):
        if not self.scope["user"].is_anonymous:
            # Remover do grupo do usuário
            await self.channel_layer.group_discard(
                self.user_group_name,
                self.channel_name
            )

    async def notification_message(self, event):
        # Enviar mensagem para o WebSocket com a contagem atualizada
        count = await self.get_unread_count()
        await self.send(text_data=json.dumps({
            'type': 'notification_message',
            'count': count
        }))

    @database_sync_to_async
    def get_unread_count(self):
        return Notification.objects.filter(
            recipient=self.scope["user"],
            read=False
        ).count()

    @database_sync_to_async
    def mark_all_as_read(self):
        Notification.objects.filter(
            recipient=self.scope["user"],
            read=False
        ).update(read=True)
        return 0  # Retorna 0 pois todas foram marcadas como lidas 