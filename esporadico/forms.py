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
        fields = ['nome_central', 'km_inicial', 'foto_inicial', 'km_final', 'local_acionamento', 'hora_inicial', 'hora_final']
        widgets = {
            'nome_central': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da central'}),
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM inicial'}),
            'km_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'KM final'}),
            'local_acionamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Local do acionamento'}),
            'foto_inicial': forms.FileInput(attrs={'class': 'form-control'}),
            'hora_inicial': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_final': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
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

class AtribuirValorForm(forms.ModelForm):
    diferenca_horas = forms.FloatField(
        label='Diferença em Horas',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'step': '0.01'
        }),
        required=False
    )
    
    diferenca_km = forms.IntegerField(
        label='Diferença em KM',
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly'
        }),
        required=False
    )
    
    class Meta:
        model = Esporadico
        fields = ['valor_atribuido']
        widgets = {
            'valor_atribuido': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o valor',
                'step': '0.01'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        
        if instance:
            # Preencher os campos de diferença automaticamente
            self.fields['diferenca_horas'].initial = instance.diferenca_horas()
            self.fields['diferenca_km'].initial = instance.diferenca_km()