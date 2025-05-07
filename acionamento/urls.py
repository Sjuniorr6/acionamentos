from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from formacompanhamento.views import api_todos_acionamentos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notifications/', include('realtime_notifications.urls')),
    path('', include('core.urls')),
    path('api/todos_acionamentos/', api_todos_acionamentos, name='api_todos_acionamentos'),
    path('formacompanhamento/', include('formacompanhamento.urls')),
]

# Configuração para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
