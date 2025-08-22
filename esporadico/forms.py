from django import forms
from django.forms import inlineformset_factory
from .models import Esporadico, FotoEsporadico

class EsporadicoCreateForm(forms.ModelForm):
    class Meta:
        model = Esporadico
        fields = ['nome_central', 'km_inicial', 'foto_inicial', 'local_acionamento']
        widgets = {
            'nome_central': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da central'}),
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM inicial'}),
            'local_acionamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do acionamento'}),
            'foto_inicial': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EsporadicoUpdateForm(forms.ModelForm):
    class Meta:
        model = Esporadico
        fields = ['nome_central', 'km_inicial', 'foto_inicial', 'km_final', 'local_acionamento']
        widgets = {
            'nome_central': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da central'}),
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM inicial'}),
            'km_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM final'}),
            'local_acionamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do acionamento'}),
            'foto_inicial': forms.FileInput(attrs={'class': 'form-control'}),
        }

class FotoEsporadicoForm(forms.ModelForm):
    class Meta:
        model = FotoEsporadico
        fields = ['foto', 'descricao']
        widgets = {
            'foto': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição da foto (opcional)'}),
        }

# Formset para múltiplas fotos
FotoEsporadicoFormSet = inlineformset_factory(
    Esporadico, 
    FotoEsporadico, 
    form=FotoEsporadicoForm,
    extra=3,  # Começar com 3 formulários vazios
    can_delete=True,
    fields=['foto', 'descricao']
)