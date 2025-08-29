from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from datetime import datetime
from .models import Esporadico, FotoEsporadico
from .forms import EsporadicoCreateForm, EsporadicoUpdateForm, FotoEsporadicoFormSet, AtribuirValorForm

# Create your views here.
class EsporadicoCreateView(LoginRequiredMixin, CreateView):
    model = Esporadico
    form_class = EsporadicoCreateForm
    template_name = 'esporadico_form.html'
    success_url = reverse_lazy('esporadico_list')
    
    def form_valid(self, form):
        form.instance.criado_por = self.request.user
        return super().form_valid(form)

class EsporadicoListView(LoginRequiredMixin, ListView):
    model = Esporadico
    template_name = 'esporadico_list.html'
    context_object_name = 'object_list'
    ordering = ['-data_acionamento']
    paginate_by = 20
    
    def get_queryset(self):
        # Filtrar apenas os registros criados pelo usuário atual
        return Esporadico.objects.filter(criado_por=self.request.user).order_by('-data_acionamento')

def esporadico_update_view(request, pk):
    esporadico = get_object_or_404(Esporadico, pk=pk)
    
    # Verificar se o usuário é o criador do registro
    if esporadico.criado_por != request.user:
        raise PermissionDenied("Você não tem permissão para editar este registro.")
    
    if request.method == 'POST':
        form = EsporadicoUpdateForm(request.POST, request.FILES, instance=esporadico)
        formset = FotoEsporadicoFormSet(request.POST, request.FILES, instance=esporadico)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, 'Acionamento esporádico atualizado com sucesso!')
            return redirect('esporadico_list')
    else:
        form = EsporadicoUpdateForm(instance=esporadico)
        formset = FotoEsporadicoFormSet(instance=esporadico)
    
    context = {
        'form': form,
        'formset': formset,
        'object': esporadico,
    }
    return render(request, 'esporadico_form.html', context)

class EsporadicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Esporadico
    template_name = 'esporadico_confirm_delete.html'
    success_url = reverse_lazy('esporadico_list')
    
    def get_queryset(self):
        # Filtrar apenas os registros criados pelo usuário atual
        return Esporadico.objects.filter(criado_por=self.request.user)

@login_required
@permission_required('formacompanhamento.view_prestadores')
def atribuir_valor_view(request, pk):
    esporadico = get_object_or_404(Esporadico, pk=pk)
    
    if request.method == 'POST':
        form = AtribuirValorForm(request.POST, instance=esporadico)
        if form.is_valid():
            form.save()
            messages.success(request, f'Valor atribuído com sucesso para {esporadico.nome_central}!')
            return redirect('esporadico_list')
    else:
        form = AtribuirValorForm(instance=esporadico)
    
    context = {
        'form': form,
        'esporadico': esporadico,
    }
    return render(request, 'esporadico_atribuir_valor.html', context)

    