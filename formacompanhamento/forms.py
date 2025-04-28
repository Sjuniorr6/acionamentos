from django import forms
from .models import Formacompanhamento, agentes
import datetime
from datetime import timedelta


# Não é necessário importar Cliente aqui, a menos que seja usado em outro lugar do código.

class formacompanhamentoForm(forms.ModelForm):
    class Meta:
        model = Formacompanhamento
        fields = ['data_inicio', 'data_final', 'prestador', 'agente', 'placa','id_equipamento','km_inicial','km_final','pedagio']
        widgets = {
            'data_inicio': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'data_final': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'prestador': forms.Select(attrs={'class': 'form-control'}),
            'agente': forms.Select(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'rows': 1}),
            'id_equipamento': forms.TextInput(attrs={'class': 'form-control', 'rows': 1}),
            'km_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'pedagio':forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
        }


class agentesForm(forms.ModelForm):
    class Meta:
        model = agentes
        fields = ['agente', 'placa', 'franquia_hora', 'franquia_km']
        widgets = {
            'agente': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'franquia_hora': forms.NumberInput(attrs={'class': 'form-control'}),  # Use NumberInput para campos numéricos
            'franquia_km': forms.NumberInput(attrs={'class': 'form-control'}),    # Use NumberInput para campos numéricos
        }


from django import forms
from datetime import timedelta
from .models import RegistroPagamento
from django import forms
from datetime import timedelta
from .models import RegistroPagamento
import re
from django import forms
from .models import Registro

class RegistroPagamentoForm(forms.ModelForm):
    class Meta:
        model = RegistroPagamento
        fields = ['cliente', 'protocolo', 'prestador', 'acionamento', 'franquia_hora', 'km_franquia', 'valor_hora_excedente', 'valor_km_excedente']
        
    cliente = forms.ModelChoiceField(queryset=Registro.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))


from django import forms
from .models import Registro, RegistroPagamento

from django import forms
from .models import RegistroPagamento

class RegistroPagamentoForm(forms.ModelForm):
    class Meta:
        model = RegistroPagamento
        fields = [
            # CAMPOS GERAIS
            'tipo_servicos','cliente', 'protocolo', 'solicitante', 'tipo_contato', 'operador',
            'modelo', 'cor', 'ano','placas1', 'descricao','placas2','placas3',
            'ultima_posicao', 'latlong', 'ultima_posicao_isca', 'latlong_isca',
            'id_isca', 'id_equipamento','motivo','endereco',

            # CAMPOS DE CONTROLE
            'quantidade_agentes', 'agentes', 'rastreador', 'isca', 'sla', 'previsa_chegada',

            # CAMPOS DO AGENTE 1
            'prestador', 'data_hora_inicial', 'data_hora_chegada', 'data_hora_final',
            'km_inicial', 'km_final', 'km_total', 'km_excedente',
            'franquia_hora', 'valor_hora_excedente', 'hora_excedente',
            'km_franquia', 'valor_km_excedente', 'valor_total_km_excedente',
            'acionamento', 'hora_total', 'pedagio','hora_total','motivo',

            # CAMPOS DO AGENTE 2
            'prestador1', 'data_hora_inicial1', 'data_hora_chegada1', 'data_hora_final1',
            'km_inicial1', 'km_final1', 'km_total1', 'km_excedente1',
            'franquia_hora1', 'valor_hora_excedente1', 'hora_excedente1',
            'km_franquia1', 'valor_km_excedente1', 'acionamento1','hora_total1','motivo1',

            # CAMPOS DO AGENTE 3
            'prestador2', 'data_hora_inicial2', 'data_hora_chegada2', 'data_hora_final2',
            'km_inicial2', 'km_final2', 'km_total2', 'km_excedente2',
            'franquia_hora2', 'valor_hora_excedente2', 'hora_excedente2',
            'km_franquia2', 'valor_km_excedente2', 'acionamento2','hora_total2','motivo2',

            # CAMPOS DO AGENTE 4
            'prestador3', 'data_hora_inicial3', 'data_hora_chegada3', 'data_hora_final3',
            'km_inicial3', 'km_final3', 'km_total3', 'km_excedente3',
            'franquia_hora3', 'valor_hora_excedente3', 'hora_excedente3',
            'km_franquia3', 'valor_km_excedente3', 'acionamento3','hora_total3','motivo3',

            # IMAGENS
            'imagem1', 'imagem2', 'imagem3', 'imagem4',
'imagem5', 'imagem6', 'imagem7', 'imagem8',
'imagem9', 'imagem10', 'imagem11', 'imagem12',
'imagem13', 'imagem14', 'imagem15', 'imagem16',
'imagem17', 'imagem18', 'imagem19', 'imagem20',
'imagem21', 'imagem22', 'imagem23', 'imagem24',
'imagem25', 'imagem26', 'imagem27', 'imagem28',
'imagem29', 'imagem30', 'imagem31', 'imagem32',
'imagem33', 'imagem34', 'imagem35', 'imagem36',
'imagem37', 'imagem38', 'imagem39', 'imagem40',
'imagem41', 'imagem42', 'imagem43', 'imagem44',
'imagem45'

        ]
        widgets = {
            # EXEMPLOS DE WIDGETS (Ajuste conforme necessário)

            'tipo_servicos': forms.Select(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'protocolo': forms.TextInput(attrs={'class': 'form-control'}),
            'solicitante': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_contato': forms.Select(attrs={'class': 'form-control'}),
            'operador': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
            'ano': forms.TextInput(attrs={'class': 'form-control'}),
            'placas1': forms.TextInput(attrs={'class': 'form-control'}),
            'placas2': forms.TextInput(attrs={'class': 'form-control'}),
            'placas3': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),

            'ultima_posicao': forms.TextInput(attrs={'class': 'form-control'}),
            'latlong': forms.TextInput(attrs={'class': 'form-control'}),
            'ultima_posicao_isca': forms.TextInput(attrs={'class': 'form-control'}),
            'latlong_isca': forms.TextInput(attrs={'class': 'form-control'}),
            'id_isca': forms.TextInput(attrs={'class': 'form-control'}),
            'id_equipamento': forms.TextInput(attrs={'class': 'form-control'}),

            'quantidade_agentes': forms.NumberInput(attrs={'class': 'form-control'}),
            'agentes': forms.NumberInput(attrs={'class': 'form-control'}),
            'rastreador': forms.Select(attrs={'class': 'form-control'}),
            'isca': forms.Select(attrs={'class': 'form-control'}),
            'sla': forms.NumberInput(attrs={'class': 'form-control'}),
            'previsa_chegada': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            # AGENTE 1
            'prestador': forms.Select(attrs={'class': 'form-control'}),
            'data_hora_inicial': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_chegada': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_final': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'km_inicial': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_final': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'hora_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_excedente': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'franquia_hora': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_hora_excedente': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_excedente': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_franquia': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_km_excedente': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_total_km_excedente': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'acionamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'pedagio': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo': forms.Select(attrs={'class': 'form-control'}),

            # AGENTE 2
            'prestador1': forms.Select(attrs={'class': 'form-control'}),
            'data_hora_inicial1': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_chegada1': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_final1': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'km_inicial1': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_final1': forms.NumberInput(attrs={'class': 'form-control'}),
             'hora_total': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_total1': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_excedente1': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'franquia_hora1': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_hora_excedente1': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_excedente1': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_franquia1': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_km_excedente1': forms.NumberInput(attrs={'class': 'form-control'}),
            'acionamento1': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo1': forms.Select(attrs={'class': 'form-control'}),

            # AGENTE 3
            'prestador2': forms.Select(attrs={'class': 'form-control'}),
            'data_hora_inicial2': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_chegada2': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_final2': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'km_inicial2': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_final2': forms.NumberInput(attrs={'class': 'form-control'}),
             'hora_tota2': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_total2': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_excedente2': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'franquia_hora2': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_hora_excedente2': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_excedente2': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_franquia2': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_km_excedente2': forms.NumberInput(attrs={'class': 'form-control'}),
            'acionamento2': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo2': forms.Select(attrs={'class': 'form-control'}),

            # AGENTE 4
            'prestador3': forms.Select(attrs={'class': 'form-control'}),
            'data_hora_inicial3': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_chegada3': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'data_hora_final3': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),

            'km_inicial3': forms.NumberInput(attrs={'class': 'form-control'}),
            'km_final3': forms.NumberInput(attrs={'class': 'form-control'}),
             'hora_total3': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_total3': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_excedente3': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'franquia_hora3': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_hora_excedente3': forms.NumberInput(attrs={'class': 'form-control'}),
            'hora_excedente3': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'km_franquia3': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_km_excedente3': forms.NumberInput(attrs={'class': 'form-control'}),
            'acionamento3': forms.NumberInput(attrs={'class': 'form-control'}),
            'motivo3': forms.Select(attrs={'class': 'form-control'}),

            # IMAGENS
            'imagem1': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem2': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem3': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem4': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem5': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem6': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem7': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem8': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem9': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem10': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem11': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem12': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem13': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem14': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem15': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem16': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem17': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem18': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem19': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem20': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem21': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem22': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem23': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem24': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem25': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem26': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem27': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem28': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem29': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem30': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem31': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem32': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem33': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem34': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem35': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem36': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem37': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem38': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem39': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem40': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem41': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem42': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem43': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem44': forms.ClearableFileInput(attrs={'class': 'form-control'}),
'imagem45': forms.ClearableFileInput(attrs={'class': 'form-control'}),

        }

        
 
        
        
from decimal import Decimal, InvalidOperation
from django import forms

class AgentePagamentoForm(forms.Form):
    prestador = forms.CharField(required=False)
    data_hora_inicial = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    data_hora_chegada = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    data_hora_final = forms.CharField(required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    franquia_hora = forms.IntegerField(required=False)
    valor_hora_excedente = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    hora_excedente = forms.CharField(required=False)
    km_inicial = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    km_final = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    km_total = forms.DecimalField(required=False, max_digits=10, decimal_places=2)
    km_excedente = forms.DecimalField(required=False, max_digits=10, decimal_places=2)

    def clean_hora_excedente(self):
        data = self.cleaned_data.get("hora_excedente")
        if data is None:
            return data
        try:
            if isinstance(data, (int, float, Decimal)):
                return Decimal(data).quantize(Decimal("0.01"))
            parts = data.split("h")
            hours = float(parts[0].strip() or 0)
            minutes = 0
            if len(parts) > 1:
                minutes = float(parts[1].replace("m", "").strip() or 0)
            total = hours + minutes / 60
            return Decimal(total).quantize(Decimal("0.01"))
        except Exception:
            raise forms.ValidationError("Formato inválido para hora excedente. Use 'Xh Ym'.")

from django.forms import formset_factory
AgentePagamentoFormSet = formset_factory(AgentePagamentoForm, extra=0, max_num=3)

import re
from datetime import timedelta
from django import forms

class SeuForm(forms.Form):
    sla = forms.CharField()  # ou outro tipo de campo apropriado para 'sla'

    def clean_sla(self):
        sla_str = self.cleaned_data.get('sla', None)
        
        if sla_str:
            try:
                # Caso o usuário insira apenas números (assumimos que seja em minutos)
                if isinstance(sla_str, str) and sla_str.isdigit():
                    minutes = int(sla_str)
                    hours, minutes = divmod(minutes, 60)
                else:
                    # Usa regex para verificar se está no formato HH:MM
                    match = re.match(r'^(\d{1,2}):(\d{2})$', sla_str)
                    if match:
                        hours, minutes = map(int, match.groups())
                    else:
                        raise ValueError('Formato inválido. Use HH:MM ou apenas minutos.')

                # Certifique-se de que os valores de horas e minutos são válidos
                if hours < 0 or minutes < 0 or minutes >= 60:
                    raise ValueError('Horas ou minutos inválidos.')

                # Converte para timedelta e retorna
                return timedelta(hours=hours, minutes=minutes)

            except ValueError as e:
                raise forms.ValidationError(str(e))

        # Caso o campo esteja vazio ou o valor não seja válido
        raise forms.ValidationError('Campo SLA não pode ser vazio.')

    def save(self, commit=True):
        # Salvar a instância do modelo
        instance = super().save(commit=False)

        # Atribuir o valor de `sla` convertido (timedelta) ao campo `sla` do modelo
        sla_timedelta = self.cleaned_data.get('sla', None)
        if sla_timedelta:
            instance.sla = sla_timedelta

        # Calcula a previsão de chegada se `data_hora_inicial` e `sla` estiverem definidos
        if instance.data_hora_inicial and instance.sla:
            instance.previsa_chegada = instance.data_hora_inicial + instance.sla

        if commit:
            instance.save()
        return instance
    

from django import forms
from .models import prestadores

from django import forms
from .models import prestadores

class PrestadoresForm(forms.ModelForm):
    class Meta:
        model = prestadores
        fields = [
            'Nome', 
            'cpf_cnpj', 
            'vencimento_cnh', 
            'tipo_prestador', 
            'endereco', 
            'cidade', 
            'estado', 
            'telefone', 
            'email', 
            'conta', 
            'disponibilidade', 
            'lat_long', 
            'status_prestador', 
            'agencia', 
            'tipo_de_conta', 
            'banco',
            'franquia_km', 
            'valor_acionamento', 
            'servicos', 
            'valor_prontaresposta_armado', 
            'franquia_hora_armado', 
            'franquia_km_armado', 
            'valorkm_armado', 
            'valorh_armado',
            'valor_prontaresposta_desarmado', 
            'franquia_hora_desarmado', 
            'franquia_km_desarmado', 
            'valorkm_desarmado', 
            'valorh_desarmado',
            'valor_antenista', 
            'franquia_hora_antenista', 
            'franquia_km_antenista', 
            'valorkm_antenista', 
            'valorh_antenista', 
            'cnh', 
            'foto'
        ]
        widgets = {
            'Nome': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Nome completo'
            }),
            'cpf_cnpj': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'CPF ou CNPJ'
            }),
            'vencimento_cnh': forms.DateInput(attrs={
                'class': 'form-control', 
                'type': 'date'
            }, format='%Y-%m-%d'),
            'tipo_prestador': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tipo de prestador'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Endereço completo'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Cidade'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control', 
                'placeholder': 'Estado'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': '(XX) XXXXX-XXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'exemplo@dominio.com'
            }),
            'conta': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Número da conta'
            }),
            'disponibilidade': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Disponibilidade'
            }),
            'lat_long': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Região de atuação'
            }),
            'status_prestador': forms.Select(attrs={'class': 'form-control'}, choices=prestadores.status),
            'agencia': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Agência'
            }),
            'tipo_de_conta': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Tipo de conta'
            }),
            'banco': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Banco'
            }),
            'franquia_km': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_acionamento': forms.NumberInput(attrs={'class': 'form-control'}),
            'servicos': forms.Select(attrs={'class': 'form-control'}, choices=prestadores.servicos_options),
            'valor_prontaresposta_armado': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Valor Pronta Resposta Armado'
            }),
            'franquia_hora_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_prontaresposta_desarmado': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Valor Pronta Resposta Desarmado'
            }),
            'franquia_hora_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valor_antenista': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Valor Antenista'
            }),
            'franquia_hora_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'cnh': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }





from django import forms
from .models import clientes_acionamento
from django import forms
from .models import clientes_acionamento

class ClientesAcionamentoForm(forms.ModelForm):
    class Meta:
        model = clientes_acionamento
        fields = [
            'nome',
            'cnpj',
            'telefone',
            'banco',
            'agencia',
            'conta',
            'servicos',
            'valor_prontaresposta_armado',
            'franquia_hora_armado',
            'franquia_km_armado',
            'valorkm_armado',
            'valorh_armado',
            'valor_prontaresposta_desarmado',
            'franquia_hora_desarmado',
            'franquia_km_desarmado',
            'valorkm_desarmado',
            'valorh_desarmado',
            'valor_antenista',
            'franquia_hora_antenista',
            'franquia_km_antenista',
            'valorkm_antenista',
            'valorh_antenista',
            'razao_social',
            'nome_fantasia',
            'inscricao_estadual',
            'inscricao_municipal',
            'atividade_principal',
            'endereco',
            'cidade',
            'estado',
            'representante_legal',
            'email_legal',
            'cpf_cnpj',
            'email_legal',
            'data_de_fechamento',
             'contato_operacional',
             'email_operacional',
             'representante_operacional',
             'contato_financeiro',
             'representante_financeiro',
             'email_financeiro',
             'contato_legal',
             'cep',
             'dias_a_faturar',
             

            # Adicionando os campos de PDF
            'contrato_pdf',
            'proposta_pdf',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'banco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Banco'}),
            'agencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Agência'}),
            'conta': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Conta'}),
            'servicos': forms.Select(attrs={'class': 'form-control'}),
            'valor_prontaresposta_armado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor PR Armado'}),
            'franquia_hora_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_armado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_armado': forms.NumberInput(attrs={'class': 'form-control'}),

            'valor_prontaresposta_desarmado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor PR Desarmado'}),
            'franquia_hora_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_desarmado': forms.NumberInput(attrs={'class': 'form-control'}),

            'valor_antenista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Valor Antenista'}),
            'franquia_hora_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'franquia_km_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorkm_antenista': forms.NumberInput(attrs={'class': 'form-control'}),
            'valorh_antenista': forms.NumberInput(attrs={'class': 'form-control'}),

            'razao_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razão Social'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome Fantasia'}),
            'inscricao_estadual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Estadual'}),
            'inscricao_municipal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inscrição Municipal'}),
            'atividade_principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Atividade Principal'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'representante_legal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'contato_legal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'representante_financeiro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'contato_financeiro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'representante_operacional': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'contato_operacional': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'data_de_fechamento': forms.DateInput(
    attrs={
        'type': 'date',
        'class': 'form-control',
        'placeholder': 'Data de Fechamento'
    }
),
            'dias_a_faturar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dias a Faturar'}),

            # Widgets para os campos de PDF (se desejar estilizar)
            'contrato_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'proposta_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


    def clean_nome(self):
        """Validação personalizada para o campo nome."""
        nome = self.cleaned_data.get('nome', '').strip()
        if len(nome) < 3:
            raise forms.ValidationError("O nome deve ter pelo menos 3 caracteres.")
        return nome

    def clean_franquiakm(self):
        """Validação personalizada para o campo franquia KM."""
        franquiakm = self.cleaned_data.get('franquiakm')
        if franquiakm is not None and franquiakm < 0:
            raise forms.ValidationError("A franquia em KM não pode ser negativa.")
        return franquiakm

    def clean_franquiahora(self):
        """Validação personalizada para o campo franquia hora."""
        franquiahora = self.cleaned_data.get('franquiahora')
        if franquiahora is not None and franquiahora < 0:
            raise forms.ValidationError("A franquia em horas não pode ser negativa.")
        return franquiahora

    def clean_valordeacionamento(self):
        """Validação personalizada para o campo valor de acionamento."""
        valordeacionamento = self.cleaned_data.get('valordeacionamento')
        if valordeacionamento is not None and valordeacionamento < 0:
            raise forms.ValidationError("O valor de acionamento não pode ser negativo.")
        return valordeacionamento

from django import forms
from .models import OcorrenciaTransporte

class OcorrenciaTransporteForm(forms.ModelForm):
    class Meta:
        model = OcorrenciaTransporte
        fields = [
            'transportadora', 'placa', 'carreta', 'motorista', 'cpf',
            'telefone', 'local', 'endereco', 'latitude', 'longitude',
            'tipo_ocorrencia', 'data_hora_ocorrencia'
        ]
        widgets = {
            'data_hora_ocorrencia': forms.DateTimeInput(
                attrs={'type': 'datetime-local'},
                format='%Y-%m-%dT%H:%M'
            ),
            'endereco': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes Bootstrap aos campos
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        
        # Máscaras e placeholders
        self.fields['cpf'].widget.attrs.update({
            'data-mask': '000.000.000-00',
            'placeholder': '000.000.000-00'
        })
        self.fields['telefone'].widget.attrs.update({
            'data-mask': '(00) 00000-0000',
            'placeholder': '(00) 00000-0000'
        })
        self.fields['placa'].widget.attrs.update({
            'placeholder': 'ABC1234',
            'pattern': '[A-Za-z]{3}[0-9][A-Za-z0-9][0-9]{2}'
        })
        self.fields['carreta'].widget.attrs.update({
            'placeholder': 'ABC1234',
            'pattern': '[A-Za-z]{3}[0-9][A-Za-z0-9][0-9]{2}'
        })

