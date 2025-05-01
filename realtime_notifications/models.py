from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    read = models.BooleanField(default=False, verbose_name='Visualizado')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Generic relation fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient}: {self.title}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:  # Apenas envia notificação se for uma nova notificação
            self.send_notification()

    def send_notification(self):
        channel_layer = get_channel_layer()
        for user in User.objects.all():
            unread_count = Notification.objects.filter(recipient=user, read=False).count()
            async_to_sync(channel_layer.group_send)(
                "notifications_all",  # Grupo global para todos os usuários
                {
                    "type": "notification_message",
                    "count": unread_count
                }
            )
