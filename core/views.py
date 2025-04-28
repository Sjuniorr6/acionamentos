from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from realtime_notifications.models import Notification
from django.contrib.auth import login

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Buscar as últimas 10 notificações do usuário
        context['notifications'] = Notification.objects.filter(
            recipient=self.request.user
        ).order_by('-created_at')[:10]
        context['unread_count'] = Notification.objects.filter(
            recipient=self.request.user, 
            read=False
        ).count()
        return context

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Redireciona após o cadastro

    def form_valid(self, form):
        """Salva o usuário e faz login automático"""
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        """Se o formulário for inválido, exibe os erros"""
        print("Formulário inválido:", form.errors)  # Debug no terminal
        return self.render_to_response(self.get_context_data(form=form))
