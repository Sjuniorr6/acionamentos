from .models import Notification

class NotificationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Buscar as últimas 10 notificações do usuário
            notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:10]
            unread_count = Notification.objects.filter(recipient=request.user, read=False).count()
            
            # Adicionar ao request para que esteja disponível em todos os templates
            request.notifications = notifications
            request.unread_notifications_count = unread_count

        response = self.get_response(request)
        return response 