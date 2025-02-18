# formacompanhamento/middleware.py
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    """
    Redireciona usuários não autenticados para a página de login,
    exceto para URLs explicitamente permitidas (login, logout, admin etc).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de caminhos (paths) que não exigem login:
        ALLOWED_PATHS = [
            reverse('login'),    # Se você usa 'django.contrib.auth.urls' e nomeou a URL de login como 'login'
            reverse('logout'),   # Se quiser permitir logout sem estar logado
            '/admin/',           # Painel admin
        ]

        # Permitir também arquivos estáticos e mídia:
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Se não estiver autenticado e não for uma URL permitida, redireciona
        if not request.user.is_authenticated:
            # Se NENHUM dos paths liberados bate com o path atual, redireciona
            if not any(request.path.startswith(path) for path in ALLOWED_PATHS):
                return redirect('login')  # ou a URL que você usa para login

        # Se estiver tudo certo (autenticado ou path liberado), segue o fluxo
        response = self.get_response(request)
        return response
