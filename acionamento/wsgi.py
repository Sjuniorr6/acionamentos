import os
import sys
from django.core.wsgi import get_wsgi_application

# Adiciona o diretório raiz do projeto ao sys.path (ajuste se necessário)
project_root = '/var/www/acionamentos'
if project_root not in sys.path:
    sys.path.append(project_root)

# Define o módulo de configurações do Django (certifique-se que o nome esteja correto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'acionamento.settings')

application = get_wsgi_application()
