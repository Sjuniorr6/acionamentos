from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from formacompanhamento.urls import all_prestadores_addresses
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('api/prestadores/enderecos/', all_prestadores_addresses, name='all_prestadores_addresses'),
    path('formacompanhamento/', include('formacompanhamento.urls')),
]

# Configuração para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
