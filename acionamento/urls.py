from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from formacompanhamento.views import api_todos_acionamentos,detalhar_acionamento_endpoint

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('realtime_notifications.urls')),
    path('', include('core.urls')),
    path('api/todos_acionamentos/', api_todos_acionamentos, name='api_todos_acionamentos'),
    path('formacompanhamento/', include('formacompanhamento.urls')),
    path('api/registro_pagamento/<int:pk>/detalhes/', detalhar_acionamento_endpoint, name='detalhar_acionamento_endpoint'),

]

# Configuração para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
