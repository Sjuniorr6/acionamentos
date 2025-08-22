from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Esporadico, FotoEsporadico
from .forms import EsporadicoCreateForm, EsporadicoUpdateForm, FotoEsporadicoFormSet

# Create your views here.
class EsporadicoCreateView(CreateView):
    model = Esporadico
    form_class = EsporadicoCreateForm
    template_name = 'esporadico_form.html'
    success_url = reverse_lazy('esporadico_list')

class EsporadicoListView(ListView):
    model = Esporadico
    template_name = 'esporadico_list.html'
    context_object_name = 'object_list'
    ordering = ['-data_acionamento']
    paginate_by = 20

def esporadico_update_view(request, pk):
    esporadico = get_object_or_404(Esporadico, pk=pk)
    
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

class EsporadicoDeleteView(DeleteView):
    model = Esporadico
    template_name = 'esporadico_confirm_delete.html'
    success_url = reverse_lazy('esporadico_list')    