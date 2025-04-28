from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification
import json

@receiver(post_save, sender=Notification)
def notification_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.recipient.id}",
            {
                "type": "notification_message",
                "count": Notification.objects.filter(
                    recipient=instance.recipient,
                    read=False
                ).count()
            }
        )

@receiver(post_save, sender=Notification)
def send_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        # Send to specific user's group
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.recipient.id}",
            {
                "type": "notification_message",
                "count": Notification.objects.filter(
                    recipient=instance.recipient,
                    read=False
                ).count()
            }
        )

@receiver(post_save, sender=Notification)
def send_notification_to_admin(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        
        # Get all admin users
        User = get_user_model()
        admin_users = User.objects.filter(is_staff=True)
        
        # Send notification to each admin user
        for user in admin_users:
            # Get unread count for the user
            unread_count = Notification.objects.filter(recipient=user, read=False).count()
            
            # Prepare notification data
            notification_data = {
                'type': 'notification_message',
                'message': {
                    'unread_count': unread_count,
                    'notification': {
                        'id': instance.id,
                        'title': instance.title,
                        'message': instance.message,
                        'timestamp': instance.created_at.isoformat(),
                        'read': instance.read,
                    }
                }
            }
            
            # Send to user's notification group
            async_to_sync(channel_layer.group_send)(
                f'notifications_{user.id}',
                notification_data
            ) 