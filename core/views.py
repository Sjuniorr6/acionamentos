from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'login'

class HomeView(TemplateView):
    template_name = 'home.html'


from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.shortcuts import render

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
