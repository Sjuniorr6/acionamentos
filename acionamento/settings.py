from pathlib import Path
import os

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta (não a exponha em produção)
SECRET_KEY = 'django-insecure-(a9zwwyq%q9n#%wq!j398bt_to7@dsc(p88t#ph=fe*330$w_$'

# DEBUG ativado para desenvolvimento (desative em produção)
DEBUG = True

# Hosts permitidos (adicione '127.0.0.1' e 'localhost' se necessário)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '107.20.1.121', 'gsacionamento.com', 'www.gsacionamento.com']

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Seu aplicativo principal
    'formacompanhamento',
    'widget_tweaks',
    
]

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'formacompanhamento.middleware.LoginRequiredMiddleware',
]

# Configuração de URL raiz
ROOT_URLCONF = 'acionamento.urls'

# Configuração dos templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],  # Pasta de templates do app "core"
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necessário para autenticação
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicação WSGI
WSGI_APPLICATION = 'acionamento.wsgi.application'

# Configuração do banco de dados (SQLite para desenvolvimento)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',  # ou o nome do banco que você definiu
        'USER': 'postgres',  # ou o usuário mestre que você criou
        'PASSWORD': '44523913',
        'HOST': 'database-1.cfegu84mu8gn.us-east-1.rds.amazonaws.com',
        'PORT': '5432',
    }
}


# Validação de senhas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configurações de internacionalização
LANGUAGE_CODE = 'pt-br'          # Idioma: Português do Brasil
TIME_ZONE = 'America/Sao_Paulo'    # Fuso horário: São Paulo
USE_I18N = True
USE_TZ = False

# Configuração dos arquivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Diretório principal para arquivos estáticos
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração para armazenar imagens na pasta `media/imagens_registros/`
MEDIA_URL = '/media/'  # URL pública para acessar as imagens
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Diretório onde as imagens serão salvas

# Configurações de redirecionamento para autenticação
LOGIN_REDIRECT_URL = 'home'       # Redireciona para a página inicial após login
LOGIN_URL = 'login'               # URL para redirecionamento em caso de acesso negado
LOGOUT_REDIRECT_URL = 'login'  # ou 'home', '/', etc.    # Redireciona para a página de login após logout

# Configuração padrão para o campo de chave primária
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
