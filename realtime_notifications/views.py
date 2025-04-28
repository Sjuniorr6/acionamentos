from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification
from django.db.models import F
from .forms import NotificationForm
from django.contrib import messages

# Create your views here.

@login_required
def notification_list(request):
    # Marcar todas as notificações como lidas ao abrir a página
    Notification.objects.filter(recipient=request.user, read=False).update(read=True)
    # Buscar todas as notificações do usuário, ordenadas por data de criação
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')
    
    # Contar notificações não lidas (deve ser zero após update)
    unread_count = Notification.objects.filter(
        recipient=request.user, 
        read=False
    ).count()
    
    return render(request, 'notifications/notification_list.html', {
        'notifications': notifications,
        'unread_count': unread_count
    })

@login_required
def get_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')[:10]
    
    unread_count = Notification.objects.filter(
        recipient=request.user, 
        read=False
    ).count()
    
    notifications_data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'read': n.read,
        'created_at': n.created_at.strftime('%d/%m/%Y %H:%M')
    } for n in notifications]
    
    return JsonResponse({
        'notifications': notifications_data,
        'unread_count': unread_count
    })

@login_required
def mark_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.read = True
        notification.save()
        
        # Retornar a nova contagem de não lidas
        unread_count = Notification.objects.filter(
            recipient=request.user, 
            read=False
        ).count()
        
        return JsonResponse({
            'status': 'success',
            'unread_count': unread_count
        })
    except Notification.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Notificação não encontrada'
        }, status=404)

@login_required
def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            messages.success(request, 'Notificação criada com sucesso!')
            return redirect('notifications:list')
    else:
        form = NotificationForm()
    
    return render(request, 'notifications/notification_form.html', {
        'form': form
    })
