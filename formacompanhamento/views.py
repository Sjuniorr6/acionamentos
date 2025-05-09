from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import RegistroPagamento, Formacompanhamento, agentes, OcorrenciaTransporte
from .forms import RegistroPagamentoForm, formacompanhamentoForm, agentesForm, OcorrenciaTransporteForm
from .utils import generate_pdf
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_GET
from decimal import Decimal
# ----------------- Forma de Acompanhamento -----------------

class formulariorateview(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Formacompanhamento
    template_name = 'formacompanhamento.html'
    form_class = formacompanhamentoForm
    context_object_name = 'acomp'
    success_url = reverse_lazy('formacompanhamento')
    permission_required = 'formacompanhamento.add_formacompanhamento'


class AcompanhamentoListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Formacompanhamento
    template_name = 'facomp.html'
    context_object_name = 'acomp'
    permission_required = 'formacompanhamento.view_formacompanhamento'


class formListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = Formacompanhamento
    template_name = 'formacompanhamento_detail.html'
    context_object_name = 'acompanhamento'
    permission_required = 'formacompanhamento.view_formacompanhamento'


# ----------------- Agentes -----------------

class agenteCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    model = agentes
    template_name = 'agentes_create.html'
    form_class = agentesForm
    context_object_name = 'agentes'
    success_url = reverse_lazy('agenteCreateView')
    permission_required = 'formacompanhamento.add_agentes'


class AgentesListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    model = agentes
    template_name = 'agentes_list.html'
    context_object_name = 'agente'
    permission_required = 'formacompanhamento.view_agentes'


class agenteUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = agentes
    template_name = 'agente_update.html'
    form_class = agentesForm
    success_url = reverse_lazy('agentesListView')
    permission_required = "formacompanhamento.view_agentes"


def get_agente_data(request, agente_id):
    agente = get_object_or_404(agentes, id=agente_id)
    data = {
        'placa': agente.placa,
    }
    return JsonResponse(data)


# ----------------- Registro de Pagamento -----------------
from django.views.generic import ListView
from formacompanhamento.models import RegistroPagamento
from .forms import AgentePagamentoForm

class RegistroPagamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistroPagamento
    template_name = 'registro_pagamento_list.html'
    context_object_name = 'registros'
    paginate_by = 10
    ordering = ['-data_hora_inicial']
    permission_required = "formacompanhamento.view_agentes"

    def get_queryset(self):
        # Pega o queryset inicial
        queryset = super().get_queryset()

        # Captura parâmetros de busca via GET
        filtro_id = self.request.GET.get('id', '').strip()
        filtro_cliente = self.request.GET.get('cliente', '').strip()
        filtro_prestador = self.request.GET.get('prestador', '').strip()
        filtro_status = self.request.GET.get('status', '').strip()
        filtro_placa = self.request.GET.get('placas1', '').strip()

        # Se o campo "id" for um número, filtra por ID exato
        if filtro_id.isdigit():
            queryset = queryset.filter(id=filtro_id)

        # Se tiver texto no campo "cliente", filtra (case-insensitive)
        if filtro_cliente:
            queryset = queryset.filter(cliente__nome__icontains=filtro_cliente)

        # Se tiver texto no campo "prestador", filtra (case-insensitive)
        if filtro_prestador:
            queryset = queryset.filter(prestador__Nome__icontains=filtro_prestador)

        # Aplica o filtro por status (case-insensitive)
        if filtro_status:
            queryset = queryset.filter(status__iexact=filtro_status)

        # Exclui registros cujo status contenha "A Faturar" ou "Pago"
        queryset = queryset.exclude(status__icontains="A Faturar") \
                           .exclude(status__icontains="Pago")

        # Mantém a lógica de atributos calculados dinamicamente
        for registro in queryset:
            registro.hora_total = registro.calcular_hora_total()
            registro.valor_total_hora_excedente = registro.calcular_valor_total_hora_excedente()
            registro.km_total = registro.calcular_km_total()
            registro.km_excedente = registro.calcular_km_excedente()
            registro.valor_total_km_excedente = registro.calcular_valor_total_km_excedente()
            registro.total_acionamento = registro.calcular_total_acionamento()
        if filtro_placa:
            queryset = queryset.filter(placas1__iexact=filtro_placa)
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Define as opções de status para o filtro no template
        context['status_choices'] = ["Início de Operação", "Em Operação", "Pendente"]
        return context



class RegistroPagamentohListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistroPagamento
    template_name = 'historico.html'
    context_object_name = 'registros'
    paginate_by = 10
    ordering = ['-data_hora_inicial']
    permission_required = "formacompanhamento.view_agentes"

    def get_queryset(self):
        # Pega o queryset inicial
        queryset = super().get_queryset()

        # Captura parâmetros de busca via GET
        filtro_id = self.request.GET.get('id', '').strip()
        filtro_cliente = self.request.GET.get('cliente', '').strip()
        filtro_prestador = self.request.GET.get('prestador', '').strip()

        # Se o campo "id" for um número, filtra por ID exato
        if filtro_id.isdigit():
            queryset = queryset.filter(id=filtro_id)

        # Se tiver texto no campo "cliente", filtra (case-insensitive)
        if filtro_cliente:
            queryset = queryset.filter(cliente__nome__icontains=filtro_cliente)

        # Se tiver texto no campo "prestador", filtra (case-insensitive)
        if filtro_prestador:
            queryset = queryset.filter(prestador__Nome__icontains=filtro_prestador)

        # Mantém a lógica de atributos calculados dinamicamente
        for registro in queryset:
            registro.hora_total = registro.calcular_hora_total()
            registro.valor_total_hora_excedente = registro.calcular_valor_total_hora_excedente()
            registro.km_total = registro.calcular_km_total()
            registro.km_excedente = registro.calcular_km_excedente()
            registro.valor_total_km_excedente = registro.calcular_valor_total_km_excedente()
            registro.total_acionamento = registro.calcular_total_acionamento()

        return queryset




from django.shortcuts import render, redirect, get_object_or_404
from .models import RegistroPagamento
from .forms import RegistroPagamentoForm, AgentePagamentoFormSet
@login_required
def registro_pagamento_update(request, pk):
    registro = get_object_or_404(RegistroPagamento, pk=pk)
    # Calcula quantos agentes adicionais existem (exemplo: se quantidade_agentes == 4, extras = 3)
    extra = max((registro.quantidade_agentes or 1) - 1, 0)
    if request.method == "POST":
        form = RegistroPagamentoForm(request.POST, request.FILES, instance=registro)
        formset = AgentePagamentoFormSet(request.POST, prefix="agentes")
        if form.is_valid() and formset.is_valid():
            registro = form.save(commit=False)
            # Processar cada formulário do formset e atribuir os dados aos campos com sufixo
            agentes_data = formset.cleaned_data
            if agentes_data:
                if len(agentes_data) >= 1:
                    data = agentes_data[0]
                    registro.prestador1 = data.get("prestador")
                    registro.data_hora_inicial1 = data.get("data_hora_inicial")
                    registro.data_hora_chegada1 = data.get("data_hora_chegada")
                    registro.data_hora_final1 = data.get("data_hora_final")
                    registro.franquia_hora1 = data.get("franquia_hora")
                    registro.valor_hora_excedente1 = data.get("valor_hora_excedente")
                    registro.hora_excedente1 = data.get("hora_excedente")
                    registro.km_inicial1 = data.get("km_inicial")
                    registro.km_final1 = data.get("km_final")
                    registro.km_total1 = data.get("km_total")
                    registro.km_excedente1 = data.get("km_excedente")
                if len(agentes_data) >= 2:
                    data = agentes_data[1]
                    registro.prestador2 = data.get("prestador")
                    registro.data_hora_inicial2 = data.get("data_hora_inicial")
                    registro.data_hora_chegada2 = data.get("data_hora_chegada")
                    registro.data_hora_final2 = data.get("data_hora_final")
                    registro.franquia_hora2 = data.get("franquia_hora")
                    registro.valor_hora_excedente2 = data.get("valor_hora_excedente")
                    registro.hora_excedente2 = data.get("hora_excedente")
                    registro.km_inicial2 = data.get("km_inicial")
                    registro.km_final2 = data.get("km_final")
                    registro.km_total2 = data.get("km_total")
                    registro.km_excedente2 = data.get("km_excedente")
                if len(agentes_data) >= 3:
                    data = agentes_data[2]
                    registro.prestador3 = data.get("prestador")
                    registro.data_hora_inicial3 = data.get("data_hora_inicial")
                    registro.data_hora_chegada3 = data.get("data_hora_chegada")
                    registro.data_hora_final3 = data.get("data_hora_final")
                    registro.franquia_hora3 = data.get("franquia_hora")
                    registro.valor_hora_excedente3 = data.get("valor_hora_excedente")
                    registro.hora_excedente3 = data.get("hora_excedente")
                    registro.km_inicial3 = data.get("km_inicial")
                    registro.km_final3 = data.get("km_final")
                    registro.km_total3 = data.get("km_total")
                    registro.km_excedente3 = data.get("km_excedente")
            registro.save()
            return redirect('formacompanhamento:registro_pagamento_list')
    else:
        form = RegistroPagamentoForm(instance=registro)
        # Preparar dados iniciais para o formset com base nos campos salvos (se houver)
        initial_data = []
        qtd = registro.quantidade_agentes or 1
        if qtd > 1:
            if registro.data_hora_inicial1 or registro.data_hora_final1 or registro.data_hora_chegada1:
                initial_data.append({
                    "prestador": registro.prestador1,
                    "data_hora_inicial": registro.data_hora_inicial1,
                    "data_hora_chegada": registro.data_hora_chegada1,
                    "data_hora_final": registro.data_hora_final1,
                    "franquia_hora": registro.franquia_hora1,
                    "valor_hora_excedente": registro.valor_hora_excedente1,
                    "hora_excedente": registro.hora_excedente1,
                    "km_inicial": registro.km_inicial1,
                    "km_final": registro.km_final1,
                    "km_total": registro.km_total1,
                    "km_excedente": registro.km_excedente1,
                })
            if qtd > 2:
                initial_data.append({
                    "prestador": registro.prestador2,
                    "data_hora_inicial": registro.data_hora_inicial2,
                    "data_hora_chegada": registro.data_hora_chegada2,
                    "data_hora_final": registro.data_hora_final2,
                    "franquia_hora": registro.franquia_hora2,
                    "valor_hora_excedente": registro.valor_hora_excedente2,
                    "hora_excedente": registro.hora_excedente2,
                    "km_inicial": registro.km_inicial2,
                    "km_final": registro.km_final2,
                    "km_total": registro.km_total2,
                    "km_excedente": registro.km_excedente2,
                })
            if qtd > 3:
                initial_data.append({
                    "prestador": registro.prestador3,
                    "data_hora_inicial": registro.data_hora_inicial3,
                    "data_hora_chegada": registro.data_hora_chegada3,
                    "data_hora_final": registro.data_hora_final3,
                    "franquia_hora": registro.franquia_hora3,
                    "valor_hora_excedente": registro.valor_hora_excedente3,
                    "hora_excedente": registro.hora_excedente3,
                    "km_inicial": registro.km_inicial3,
                    "km_final": registro.km_final3,
                    "km_total": registro.km_total3,
                    "km_excedente": registro.km_excedente3,
                })
        from django.forms import formset_factory
        AgentePagamentoFormSet = formset_factory(AgentePagamentoForm, extra=0, max_num=3)
        formset = AgentePagamentoFormSet(initial=initial_data, prefix="agentes")
    
    return render(request, 'registro_pagamento_form.html', {'form': form, 'formset': formset})

from datetime import timedelta
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import RegistroPagamento
from .forms import RegistroPagamentoForm
import logging

logger = logging.getLogger(__name__)
from datetime import timedelta
import logging
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import RegistroPagamento, prestadores  # ajuste conforme sua organização
from .forms import RegistroPagamentoForm

logger = logging.getLogger(__name__)

class RegistroPagamentoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = RegistroPagamento
    form_class = RegistroPagamentoForm
    template_name = 'registro_pagamento_form.html'
    success_url = reverse_lazy('formacompanhamento:registro_pagamento_list')
    permission_required = "formacompanhamento.view_agentes"

    def form_valid(self, form):
        # Debug: imprimir os dados recebidos no POST
        print("POST RECEBIDO:", self.request.POST)
        
        # Cria a instância sem salvar imediatamente
        instance = form.save(commit=False)

        # Adiciona os valores dos campos adicionais de motivo
        instance.motivo1 = form.cleaned_data.get("motivo1")
        instance.motivo2 = form.cleaned_data.get("motivo2")
        instance.motivo3 = form.cleaned_data.get("motivo3")

        # Se o formulário já enviou um valor para previsa_chegada (preenchido via JavaScript),
        # usa-o; caso contrário, calcula com base em data_hora_inicial e sla.
        if not form.cleaned_data.get("previsa_chegada"):
            if instance.data_hora_inicial and instance.sla:
                try:
                    if isinstance(instance.sla, timedelta):
                        instance.previsa_chegada = instance.data_hora_inicial + instance.sla
                    else:
                        instance.previsa_chegada = instance.data_hora_inicial + timedelta(minutes=int(instance.sla))
                except (ValueError, TypeError) as e:
                    logger.error("Erro ao calcular previsa_chegada: %s", e)
                    instance.previsa_chegada = None
                    form.add_error('sla', 'SLA inválido ou mal formatado.')
        # Caso contrário, o valor vindo do formulário (preenchido pelo JavaScript) é mantido.

        # Cálculo de hora_total (em horas), se os campos necessários estiverem preenchidos
        if instance.data_hora_inicial and instance.data_hora_final:
            try:
                duration = instance.data_hora_final - instance.data_hora_inicial
                instance.hora_total = round(duration.total_seconds() / 3600, 2)
            except Exception as e:
                logger.error("Erro ao calcular hora_total: %s", e)
                instance.hora_total = 0

        # Cálculo de km_total e km_excedente, se os campos de quilometragem estiverem preenchidos
        if instance.km_inicial is not None and instance.km_final is not None:
            try:
                instance.km_total = max(instance.km_final - instance.km_inicial, 0)
                if instance.km_franquia is not None:
                    instance.km_excedente = max(instance.km_total - instance.km_franquia, 0)
                else:
                    instance.km_excedente = 0
            except Exception as e:
                logger.error("Erro ao calcular km_total ou km_excedente: %s", e)
                instance.km_total = 0
                instance.km_excedente = 0

        # Salva a instância modificada
        try:
            instance.save()
            self.object = instance
            logger.info("Registro criado com sucesso: %s", instance.id)
        except Exception as e:
            logger.error("Erro ao salvar o registro no banco de dados: %s", e)
            return self.form_invalid(form)

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        logger.error("Erro ao validar o formulário:")
        for field, errors in form.errors.items():
            logger.error("%s: %s", field, errors)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Gerar os nomes dos campos dinamicamente para os agentes
        quantidade_agentes = 4  # Exemplo de quantidade de agentes
        agentes_lista = list(range(1, quantidade_agentes + 1))
        campos_dinamicos = [
            'prestador',
            'data_hora_inicial',
            'data_hora_chegada',
            'data_hora_final',
            'km_inicial',
            'km_final',
            'motivo'  # Inclui o motivo para cada agente
        ]
        campos = {}
        for i in agentes_lista:
            for campo in campos_dinamicos:
                campos[f'{campo}{i}'] = f'{campo}{i}'
        context['agentes_lista'] = agentes_lista
        context['campos'] = campos
        return context

from django.shortcuts import render, get_object_or_404
from .models import RegistroPagamento
from django.shortcuts import render, get_object_or_404
from .models import RegistroPagamento
@login_required
def detalhar_acionamento(request, pk):
    registro = get_object_or_404(RegistroPagamento, pk=pk)
    cliente = registro.cliente

    # Função auxiliar para tratar campos vazios
    def format_field(value, default="Não informado"):
        if value is None or str(value).strip() == "":
            return default
        return str(value).strip()

    # Dados do Cliente (utilize os nomes exatos dos campos do seu modelo)
    client_data = {
        'nome': format_field(cliente.nome),
        'cnpj': format_field(cliente.cnpj),
        'telefone': format_field(cliente.telefone),
        'banco': format_field(cliente.banco),
        'agencia': format_field(cliente.agencia),
        'conta': format_field(cliente.conta),
        'servicos': format_field(cliente.servicos),
        'valor_prontaresposta_armado': format_field(cliente.valor_prontaresposta_armado),
        'franquia_hora_armado': format_field(cliente.franquia_hora_armado),
        'franquia_km_armado': format_field(cliente.franquia_km_armado),
        'valorkm_armado': format_field(cliente.valorkm_armado),
        'valorh_armado': format_field(cliente.valorh_armado),
        'valor_prontaresposta_desarmado': format_field(cliente.valor_prontaresposta_desarmado),
        'franquia_hora_desarmado': format_field(cliente.franquia_hora_desarmado),
        'franquia_km_desarmado': format_field(cliente.franquia_km_desarmado),
        'valorkm_desarmado': format_field(cliente.valorkm_desarmado),
        'valorh_desarmado': format_field(cliente.valorh_desarmado),
        'valor_antenista': format_field(cliente.valor_antenista),
        'franquia_hora_antenista': format_field(cliente.franquia_hora_antenista),
        'franquia_km_antenista': format_field(cliente.franquia_km_antenista),
        'valorkm_antenista': format_field(cliente.valorkm_antenista),
        'valorh_antenista': format_field(cliente.valorh_antenista),
    }

    # Dados do Agente Principal (assumindo que esses campos estão no registro)
    main_agent_data = {
        'nome': format_field(registro.prestador),
        'cnpj': format_field(getattr(registro, 'cnpj', None)),
        'telefone': format_field(getattr(registro, 'telefone', None)),
        'banco': format_field(getattr(registro, 'banco', None)),
        'agencia': format_field(getattr(registro, 'agencia', None)),
        'conta': format_field(getattr(registro, 'conta', None)),
        'servicos': format_field(getattr(registro, 'servicos', None)),
        'valor_prontaresposta_armado': format_field(getattr(registro, 'valor_prontaresposta_armado', None)),
        'franquia_hora_armado': format_field(getattr(registro, 'franquia_hora_armado', None)),
        'franquia_km_armado': format_field(getattr(registro, 'franquia_km_armado', None)),
        'valorkm_armado': format_field(getattr(registro, 'valorkm_armado', None)),
        'valorh_armado': format_field(getattr(registro, 'valorh_armado', None)),
        'valor_prontaresposta_desarmado': format_field(getattr(registro, 'valor_prontaresposta_desarmado', None)),
        'franquia_hora_desarmado': format_field(getattr(registro, 'franquia_hora_desarmado', None)),
        'franquia_km_desarmado': format_field(getattr(registro, 'franquia_km_desarmado', None)),
        'valorkm_desarmado': format_field(getattr(registro, 'valorkm_desarmado', None)),
        'valorh_desarmado': format_field(getattr(registro, 'valorh_desarmado', None)),
        'valor_antenista': format_field(getattr(registro, 'valor_antenista', None)),
        'franquia_hora_antenista': format_field(getattr(registro, 'franquia_hora_antenista', None)),
        'franquia_km_antenista': format_field(getattr(registro, 'franquia_km_antenista', None)),
        'valorkm_antenista': format_field(getattr(registro, 'valorkm_antenista', None)),
        'valorh_antenista': format_field(getattr(registro, 'valorh_antenista', None)),
        'data_hora_inicial': registro.data_hora_inicial,
        'data_hora_chegada': registro.data_hora_chegada,
        'data_hora_final': registro.data_hora_final,
        'km_inicial': registro.km_inicial,
        'km_final': registro.km_final,
        'km_total': registro.km_total,
        'hora_total': registro.hora_total,
        'motivo': registro.motivo,
    }

    # Dados dos Agentes Adicionais
    # Exemplo: espera-se que os campos para o 1º agente adicional sejam 'prestador1', 'cnpj1', etc.
    quantidade_agentes = 4
    additional_agents = []
    for i in range(1, quantidade_agentes + 1):
        if getattr(registro, f'prestador{i}', None):
            agent_data = {
                'nome': format_field(getattr(registro, f'prestador{i}', None)),
                'cnpj': format_field(getattr(registro, f'cnpj{i}', None)),
                'telefone': format_field(getattr(registro, f'telefone{i}', None)),
                'banco': format_field(getattr(registro, f'banco{i}', None)),
                'agencia': format_field(getattr(registro, f'agencia{i}', None)),
                'conta': format_field(getattr(registro, f'conta{i}', None)),
                'servicos': format_field(getattr(registro, f'servicos{i}', None)),
                'valor_prontaresposta_armado': format_field(getattr(registro, f'valor_prontaresposta_armado{i}', None)),
                'franquia_hora_armado': format_field(getattr(registro, f'franquia_hora_armado{i}', None)),
                'franquia_km_armado': format_field(getattr(registro, f'franquia_km_armado{i}', None)),
                'valorkm_armado': format_field(getattr(registro, f'valorkm_armado{i}', None)),
                'valorh_armado': format_field(getattr(registro, f'valorh_armado{i}', None)),
                'valor_prontaresposta_desarmado': format_field(getattr(registro, f'valor_prontaresposta_desarmado{i}', None)),
                'franquia_hora_desarmado': format_field(getattr(registro, f'franquia_hora_desarmado{i}', None)),
                'franquia_km_desarmado': format_field(getattr(registro, f'franquia_km_desarmado{i}', None)),
                'valorkm_desarmado': format_field(getattr(registro, f'valorkm_desarmado{i}', None)),
                'valorh_desarmado': format_field(getattr(registro, f'valorh_desarmado{i}', None)),
                'valor_antenista': format_field(getattr(registro, f'valor_antenista{i}', None)),
                'franquia_hora_antenista': format_field(getattr(registro, f'franquia_hora_antenista{i}', None)),
                'franquia_km_antenista': format_field(getattr(registro, f'franquia_km_antenista{i}', None)),
                'valorkm_antenista': format_field(getattr(registro, f'valorkm_antenista{i}', None)),
                'valorh_antenista': format_field(getattr(registro, f'valorh_antenista{i}', None)),
                'motivo': format_field(getattr(registro, f'motivo{i}', None)),
            }
            additional_agents.append(agent_data)

    context = {
        'registro': registro,
        'client_data': client_data,
        'main_agent': main_agent_data,
        'additional_agents': additional_agents,
    }
    return render(request, 'detalhar_acionamento.html', context)




from django.shortcuts import render
from .models import RegistroPagamento
    
from django.shortcuts import render
from .models import RegistroPagamento


# Na sua view
# Na sua view

# Na sua view, crie a lista de campos dinamicamente e passe para o template
@login_required
def registro_pagamento_create(request):
    quantidade_agentes = 4  # Este valor pode ser obtido dinamicamente
    agentes_lista = list(range(1, quantidade_agentes + 1))  # Lista de 1 até a quantidade de agentes

    return render(request, 'formacompanhamento/registro_pagamento_form.html', {
        'agentes_lista': agentes_lista,  # Passe a lista de agentes para o template
    })



# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import prestadores

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import prestadores
@login_required
def prestador_detail(request):
    # Obter o ID do prestador da query string: ?id=...
    prestador_id = request.GET.get('id')
    if not prestador_id:
        return JsonResponse({'error': 'ID não fornecido.'}, status=400)
    
    prestador = get_object_or_404(prestadores, pk=prestador_id)
    
    # Monte o dicionário com todos os campos desejados.
    data = {
        'Nome': prestador.Nome,
        'cpf_cnpj': prestador.cpf_cnpj,
        'vencimento_cnh': prestador.vencimento_cnh.strftime('%Y-%m-%d') if prestador.vencimento_cnh else None,
        'tipo_prestador': prestador.tipo_prestador,
        'endereco': prestador.endereco,
        'telefone': prestador.telefone,
        'email': prestador.email,
        'conta': prestador.conta,
        'disponibilidade': prestador.disponibilidade,
        'lat_long': prestador.lat_long,
        'status_prestador': prestador.status_prestador,
        'agencia': prestador.agencia,
        'tipo_de_conta': prestador.tipo_de_conta,
        'banco': prestador.banco,
        'franquia_km': str(prestador.franquia_km) if prestador.franquia_km is not None else None,
        'valor_acionamento': str(prestador.valor_acionamento) if prestador.valor_acionamento is not None else None,
        'servicos': prestador.servicos,
        'valor_prontaresposta_armado': prestador.valor_prontaresposta_armado,
        'franquia_hora_armado': str(prestador.franquia_hora_armado) if prestador.franquia_hora_armado is not None else None,
        'franquia_km_armado': str(prestador.franquia_km_armado) if prestador.franquia_km_armado is not None else None,
        'valorkm_armado': str(prestador.valorkm_armado) if prestador.valorkm_armado is not None else None,
        'valorh_armado': str(prestador.valorh_armado) if prestador.valorh_armado is not None else None,
        'valor_prontaresposta_desarmado': prestador.valor_prontaresposta_desarmado,
        'franquia_hora_desarmado': str(prestador.franquia_hora_desarmado) if prestador.franquia_hora_desarmado is not None else None,
        'franquia_km_desarmado': str(prestador.franquia_km_desarmado) if prestador.franquia_km_desarmado is not None else None,
        'valorkm_desarmado': str(prestador.valorkm_desarmado) if prestador.valorkm_desarmado is not None else None,
        'valorh_desarmado': str(prestador.valorh_desarmado) if prestador.valorh_desarmado is not None else None,
        'valor_antenista': prestador.valor_antenista,
        'franquia_hora_antenista': str(prestador.franquia_hora_antenista) if prestador.franquia_hora_antenista is not None else None,
        'franquia_km_antenista': str(prestador.franquia_km_antenista) if prestador.franquia_km_antenista is not None else None,
        'valorkm_antenista': str(prestador.valorkm_antenista) if prestador.valorkm_antenista is not None else None,
        'valorh_antenista': str(prestador.valorh_antenista) if prestador.valorh_antenista is not None else None,
    }
    
    return JsonResponse(data)







# Função auxiliar para buscar dados do prestador
from django.http import JsonResponse
from django.apps import apps
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import prestadores  # Certifique-se de que está importando corretamente

def get_prestador_data(request):
    prestador_id = request.GET.get('id')
    if not prestador_id:
        return JsonResponse({'error': 'ID não fornecido.'}, status=400)
    
    prestador = get_object_or_404(prestadores, pk=prestador_id)
    
    # Retornar todos os campos desejados.
    # Para campos do tipo Decimal, convertemos para string.
    data = {
        'Nome': prestador.Nome,
        'cpf_cnpj': prestador.cpf_cnpj,
        'vencimento_cnh': prestador.vencimento_cnh.isoformat() if prestador.vencimento_cnh else None,
        'tipo_prestador': prestador.tipo_prestador,
        'endereco': prestador.endereco,
        'telefone': prestador.telefone,
        'email': prestador.email,
        'conta': prestador.conta,
        'disponibilidade': prestador.disponibilidade,
        'lat_long': prestador.lat_long,
        'status_prestador': prestador.status_prestador,
        'agencia': prestador.agencia,
        'tipo_de_conta': prestador.tipo_de_conta,
        'banco': prestador.banco,
        'franquia_km': str(prestador.franquia_km) if prestador.franquia_km is not None else None,
        'valor_acionamento': str(prestador.valor_acionamento) if prestador.valor_acionamento is not None else None,
        'servicos': prestador.servicos,
        'valor_prontaresposta_armado': prestador.valor_prontaresposta_armado,
        'franquia_hora_armado': str(prestador.franquia_hora_armado) if prestador.franquia_hora_armado is not None else None,
        'franquia_km_armado': str(prestador.franquia_km_armado) if prestador.franquia_km_armado is not None else None,
        'valorkm_armado': str(prestador.valorkm_armado) if prestador.valorkm_armado is not None else None,
        'valorh_armado': str(prestador.valorh_armado) if prestador.valorh_armado is not None else None,
        'valor_prontaresposta_desarmado': prestador.valor_prontaresposta_desarmado,
        'franquia_hora_desarmado': str(prestador.franquia_hora_desarmado) if prestador.franquia_hora_desarmado is not None else None,
        'franquia_km_desarmado': str(prestador.franquia_km_desarmado) if prestador.franquia_km_desarmado is not None else None,
        'valorkm_desarmado': str(prestador.valorkm_desarmado) if prestador.valorkm_desarmado is not None else None,
        'valorh_desarmado': str(prestador.valorh_desarmado) if prestador.valorh_desarmado is not None else None,
        'valor_antenista': prestador.valor_antenista,
        'franquia_hora_antenista': str(prestador.franquia_hora_antenista) if prestador.franquia_hora_antenista is not None else None,
        'franquia_km_antenista': str(prestador.franquia_km_antenista) if prestador.franquia_km_antenista is not None else None,
        'valorkm_antenista': str(prestador.valorkm_antenista) if prestador.valorkm_antenista is not None else None,
        'valorh_antenista': str(prestador.valorh_antenista) if prestador.valorh_antenista is not None else None,
    }
    
    return JsonResponse(data)
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import RegistroPagamento
from .forms import RegistroPagamentoForm
from .models import clientes_acionamento


class RegistroPagamentoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = RegistroPagamento
    form_class = RegistroPagamentoForm
    template_name = 'registro_pagamento_update.html'  # Seu template de edição
    success_url = reverse_lazy('formacompanhamento:registro_pagamento_list')  # Redireciona após salvar
    permission_required = "formacompanhamento.view_agentes"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        filled_fields = []
        # Itera sobre os campos definidos no formulário
        for field_name in self.form_class.base_fields:
            # Obtém o valor do campo na instância (caso seja None ou string vazia, não é considerado preenchido)
            value = getattr(instance, field_name, None)
            if value not in [None, '', []]:
                filled_fields.append(field_name)
        context['filled_fields'] = filled_fields
        return context

    def form_valid(self, form):
        return super().form_valid(form)





from django.views.generic.edit import UpdateView
from .models import clientes_acionamento
from .forms import ClientesAcionamentoForm
from django.urls import reverse_lazy

class ClienteUpdateView(UpdateView):
    model = clientes_acionamento
    form_class = ClientesAcionamentoForm
    template_name = 'update_clientes_acionamento.html'
    success_url = reverse_lazy('formacompanhamento:clientes_acionamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Inclui as variáveis que são necessárias no template
        context['form'] = self.get_form()
        return context
class RegistroPagamentoDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = RegistroPagamento
    template_name = 'registro_pagamento_confirm_delete.html'
    success_url = reverse_lazy('registro_pagamento_list')
    permission_required = "formacompanhamento.view_agentes"

def validar(request, pk):
    registro = get_object_or_404(RegistroPagamento, pk=pk)
    registro.status = "A Faturar"  # Atualize o status do registro
    registro.save()
    return redirect('formacompanhamento:registro_pagamento_list')


# ----------------- Atualização de Registro -----------------
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from formacompanhamento.models import Registro

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Registro, clientes_acionamento
from django.shortcuts import render, redirect
from .models import Registro, clientes_acionamento
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def nova_tabela_view(request):
    """
    View para renderizar a tabela com os registros existentes e carregar os clientes.
    Também permite criar novos registros via formulário.
    """
    registros = Registro.objects.all()  # Busca todos os registros
    clientes = clientes_acionamento.objects.all()  # Busca todos os clientes

    if request.method == "POST":
        form = RegistroPagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nova_tabela')  # Redireciona para a mesma página após salvar
    else:
        form = RegistroPagamentoForm()

    return render(request, 'nova_tabela.html', {
        'registros': registros,
        'clientes': clientes,
        'form': form  # Formulário para criar um novo registro
    })


@csrf_exempt
def atualizar_registro(request):
    """
    View para atualizar os registros via requisição AJAX.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Dados recebidos no backend:", data)  # Log para depuração

            registro_id = data.get('id')
            if not registro_id:
                return JsonResponse({'error': 'ID é obrigatório.'}, status=400)

            # Recupera o registro no banco de dados
            registro = Registro.objects.filter(id=registro_id).first()
            if not registro:
                return JsonResponse({'error': 'Registro não encontrado.'}, status=404)

            # Atualiza os campos do registro
            registro.hora_excedente = data.get('hora_excedente', registro.hora_excedente)
            registro.valor_hora_excedente = data.get('valor_hora_excedente', registro.valor_hora_excedente)
            registro.km_excedente = data.get('km_excedente', registro.km_excedente)
            registro.valor_km_excedente = data.get('valor_km_excedente', registro.valor_km_excedente)
            registro.acionamento = data.get('acionamento', registro.acionamento)
            registro.total_cliente = data.get('total_cliente', registro.total_cliente)
            registro.save()  # Salva no banco

            return JsonResponse({'message': 'Registro atualizado com sucesso!'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido.'}, status=400)
        except Exception as e:
            print("Erro no backend:", str(e))  # Log para depuração
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método não permitido.'}, status=405)




def download_pdf(request, pk):
    registro = get_object_or_404(RegistroPagamento, pk=pk)
    pdf = generate_pdf(registro)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="registro_pagamento_{registro.id}.pdf"'
    return response


# ----------------- Nova Tabela -----------------









from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.http import HttpResponse
from .forms import RegistroPagamentoForm
from .models import RegistroPagamento
from .utils import generate_pdf  # Certifique-se de que esta função existe

class FormularioView(PermissionRequiredMixin,LoginRequiredMixin,FormView):
    template_name = "registro_pagamento_form.html"  # Altere para o template correto do formulário
    form_class = RegistroPagamentoForm
    permission_required = "formacompanhamento.view_agentes"
    def form_valid(self, form):
        # Salva o formulário no banco de dados e cria uma instância
        instance = form.save()

        # Gera o PDF com os dados do registro salvo
        pdf = generate_pdf(instance)

        # Verifica se o PDF foi gerado corretamente
        if not pdf:
            return HttpResponse("Erro ao gerar o PDF.", status=500)

        # Retorna o PDF como resposta para download
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="relatorio_{instance.id}.pdf"'
        return response








from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import prestadores
from .forms import PrestadoresForm

from django.http import HttpResponseNotAllowed
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import prestadores
from .forms import PrestadoresForm

from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed
from .models import prestadores
from .forms import PrestadoresForm
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
import logging
from .models import prestadores
from .forms import PrestadoresForm

from django.contrib import messages

class PrestadorCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = prestadores
    form_class = PrestadoresForm
    template_name = 'formulario_prestador.html'
    success_url = reverse_lazy('formacompanhamento:lista_prestadores')
    permission_required = "formacompanhamento.view_agentes"

    def form_valid(self, form):
        try:
            # Salva o novo prestador
            response = super().form_valid(form)
            message = f"Prestador {form.instance.Nome} criado com sucesso (ID: {form.instance.id})"
            # Adiciona a mensagem de sucesso
            messages.success(self.request, message)
            return response
        except Exception as e:
            # Caso ocorra algum erro, loga a exceção
            message = f"Erro ao criar o prestador: {e}"
            messages.error(self.request, message)
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print("Erros do Formulário:", form.errors)  # Debug para ver o que está errado
        messages.error(self.request, f"Formulário inválido. Erros: {form.errors}")
        return super().form_invalid(form)



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import prestadores

def prestador_detail(request):
    # Obter o ID do prestador a partir da query string (?id=...)
    prestador_id = request.GET.get('id')
    if not prestador_id:
        return JsonResponse({'error': 'ID não fornecido.'}, status=400)
    
    prestador = get_object_or_404(prestadores, pk=prestador_id)
    
    # Retornar todos os campos desejados.
    # Para campos do tipo Decimal, convertemos para string.
    data = {
        'Nome': prestador.Nome,
        'cpf_cnpj': prestador.cpf_cnpj,
        'vencimento_cnh': prestador.vencimento_cnh.isoformat() if prestador.vencimento_cnh else None,
        'tipo_prestador': prestador.tipo_prestador,
        'endereco': prestador.endereco,
        'telefone': prestador.telefone,
        'email': prestador.email,
        'conta': prestador.conta,
        'disponibilidade': prestador.disponibilidade,
        'lat_long': prestador.lat_long,
        'status_prestador': prestador.status_prestador,
        'agencia': prestador.agencia,
        'tipo_de_conta': prestador.tipo_de_conta,
        'banco': prestador.banco,
        'franquia_km': str(prestador.franquia_km) if prestador.franquia_km is not None else None,
        'valor_acionamento': str(prestador.valor_acionamento) if prestador.valor_acionamento is not None else None,
        'servicos': prestador.servicos,
        'valor_prontaresposta_armado': prestador.valor_prontaresposta_armado,
        'franquia_hora_armado': str(prestador.franquia_hora_armado) if prestador.franquia_hora_armado is not None else None,
        'franquia_km_armado': str(prestador.franquia_km_armado) if prestador.franquia_km_armado is not None else None,
        'valorkm_armado': str(prestador.valorkm_armado) if prestador.valorkm_armado is not None else None,
        'valorh_armado': str(prestador.valorh_armado) if prestador.valorh_armado is not None else None,
        'valor_prontaresposta_desarmado': prestador.valor_prontaresposta_desarmado,
        'franquia_hora_desarmado': str(prestador.franquia_hora_desarmado) if prestador.franquia_hora_desarmado is not None else None,
        'franquia_km_desarmado': str(prestador.franquia_km_desarmado) if prestador.franquia_km_desarmado is not None else None,
        'valorkm_desarmado': str(prestador.valorkm_desarmado) if prestador.valorkm_desarmado is not None else None,
        'valorh_desarmado': str(prestador.valorh_desarmado) if prestador.valorh_desarmado is not None else None,
        'valor_antenista': prestador.valor_antenista,
        'franquia_hora_antenista': str(prestador.franquia_hora_antenista) if prestador.franquia_hora_antenista is not None else None,
        'franquia_km_antenista': str(prestador.franquia_km_antenista) if prestador.franquia_km_antenista is not None else None,
        'valorkm_antenista': str(prestador.valorkm_antenista) if prestador.valorkm_antenista is not None else None,
        'valorh_antenista': str(prestador.valorh_antenista) if prestador.valorh_antenista is not None else None,
    }
    
    return JsonResponse(data)


from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import prestadores  # Substitua "prestadores" pelo nome correto do seu modelo, se necessário


class PrestadorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = prestadores
    template_name = 'lista_prestadores.html'
    context_object_name = 'prestadores'
    permission_required = "formacompanhamento.view_agentes"

    def get_queryset(self):
        qs = super().get_queryset()

        servicos = self.request.GET.get('servicos', '')
        nome = self.request.GET.get('nome', '')  # Corrigido aqui
        estado = self.request.GET.get('estado', '').upper().strip()  # Corrigido aqui e padronizado para uppercase

        if servicos:
            qs = qs.filter(servicos__icontains=servicos)
        if nome:
            qs = qs.filter(Nome__icontains=nome)
        if estado:
            qs = qs.filter(estado__iexact=estado)

        return qs


    from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import clientes_acionamento
from .forms import ClientesAcionamentoForm
from .forms import ClientesAcionamentoForm


class ClientesAcionamentoCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = clientes_acionamento
    form_class = ClientesAcionamentoForm
    template_name = 'create_clientes_acionamento.html'
    success_url = reverse_lazy('formacompanhamento:clientes_acionamento_list')
    permission_required = "formacompanhamento.view_agentes"
   
from django.views.generic import ListView


class ClientesAcionamentoListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = clientes_acionamento
    template_name = 'clientes_acionamento_list.html'
    context_object_name = 'clientes'
    permission_required = "formacompanhamento.view_agentes"
    
    
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .utils import generate_pdf
from .models import RegistroPagamento
import logging

logger = logging.getLogger(__name__)

def download_pdf(request, instance_id):
    """
    Gera e retorna o PDF para download com base na instância do RegistroPagamento.
    """
    registro = get_object_or_404(RegistroPagamento, pk=instance_id)

    try:
        # Gera o PDF
        pdf = generate_pdf(registro)
    except Exception as e:
        logger.error(f"Erro ao gerar PDF para o registro {instance_id}: {e}")
        return HttpResponse("Erro ao gerar o PDF.", status=500)

    # Configura a resposta HTTP para download
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="registro_pagamento_{registro.id}.pdf"'
    return response


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import RegistroPagamento

def obter_dados_registro(request, registro_id):
    registro = get_object_or_404(RegistroPagamento, id=registro_id)
    dados = {
        "total_acionamento": float(registro.calcular_total_acionamento()),
        "km_excedente": float(registro.calcular_km_excedente()),
        "hora_excedente": float(registro.calcular_hora_excedente()),
    }
    return JsonResponse(dados)

from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from .models import RegistroPagamento, clientes_acionamento, TotalRegistro
from django.http import HttpResponse

class TotalFormView(TemplateView):
    template_name = 'total.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registros'] = RegistroPagamento.objects.all()
        context['clientes'] = clientes_acionamento.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        registro_id = request.GET.get('registro_id')
        if registro_id:
            registro = get_object_or_404(RegistroPagamento, id=registro_id)
            return JsonResponse({
                "total_acionamento": float(registro.total_acionamento),
                "km_excedente": float(registro.km_excedente),
                "hora_excedente": float(registro.hora_excedente),
                "valor_km_excedente": float(registro.valor_total_km_excedente),
                "valor_hora_excedente": float(registro.calcular_valor_total_hora_excedente()),
            })
        return super().get(request, *args, **kwargs)
        



from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import RegistroPagamento  # Ajuste conforme o nome do modelo


def registro_dados(request, registro_id):
    """
    Retorna os dados do registro em JSON.
    """
    registro = get_object_or_404(RegistroPagamento, id=registro_id)

    # Garantir que os valores são calculados ao acessar
    registro.save()  # Força a reexecução do cálculo

    dados = {
        "total_acionamento": float(registro.total_acionamento or 0.0),
        "km_excedente": float(registro.km_excedente or 0.0),
        "hora_excedente": float(registro.hora_excedente or 0.0),
    }

    return JsonResponse(dados)


from django.http import JsonResponse, Http404

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import clientes_acionamento


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from .models import clientes_acionamento

def obter_dados_cliente(request, cliente_id):
    """
    Retorna todos os dados do cliente em JSON, convertendo os campos decimais para float.
    """
    cliente = get_object_or_404(clientes_acionamento, id=cliente_id)
    dados = model_to_dict(cliente)

    # Lista com os nomes dos campos que são DecimalField e precisam ser convertidos para float
    campos_decimais = [
        'valor_prontaresposta_armado'
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
        'valorh_antenista'
    ]

    for campo in campos_decimais:
        # Se o valor existir, converte para float; caso contrário, define como 0.0 ou mantenha None
        if dados.get(campo) is not None:
            dados[campo] = float(dados[campo])
        else:
            dados[campo] = 0.0

    return JsonResponse(dados)


from django.shortcuts import render
from .models import RegistroPagamento, clientes_acionamento

# views.py




from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from .models import RegistroPagamento, clientes_acionamento

from django.views.generic import TemplateView
from .models import clientes_acionamento, RegistroPagamento

class TabelaRegistrosView(LoginRequiredMixin,PermissionRequiredMixin,TemplateView):
    template_name = 'tabela_registros.html'  # Nome do template a ser renderizado
    paginate_by = 10
    permission_required = "formacompanhamento.view_agentes"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Adicionar dados do primeiro modelo
        context['registros'] = TotalRegistro.objects.all()

        

        return context


        

class prestadoresupdate(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = prestadores
    form_class = PrestadoresForm
    template_name = 'prestadores_update.html'
    success_url = reverse_lazy('formacompanhamento:lista_prestadores')
    permission_required = "formacompanhamento.view_agentes"
    
    
    
    
    
    
    
    
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import RegistroPagamento

from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_naive, make_aware

@require_GET
def detalhar_acionamento_endpoint(request, pk):
    def format_field(value, default="Não informado"):
        return str(value) if value is not None else default

    def format_datetime_field(dt):
        if not dt:
            return ""
        if isinstance(dt, str):
            return dt
        try:
            if is_naive(dt):
                dt = make_aware(dt)
            return dt.isoformat()
        except Exception:
            return str(dt)

    def parse_decimal(value):
        if not value or value == "Não informado":
            return Decimal('0')
        try:
            return Decimal(str(value).replace(',', '.'))
        except (InvalidOperation, TypeError):
            return Decimal('0')

    def diferenca_horas(inicio, fim):
        if not inicio or not fim:
            return Decimal('0')
        try:
            if isinstance(inicio, str):
                inicio = parse_datetime(inicio)
            if isinstance(fim, str):
                fim = parse_datetime(fim)
            if not inicio or not fim:
                return Decimal('0')
            diff = fim - inicio
            return Decimal(str(diff.total_seconds() / 3600))
        except (ValueError, TypeError):
            return Decimal('0')

    def calcular_total_agente(motivo, agente, prestador):
        hora_exc = parse_decimal(agente.get('hora_excedente'))
        km_exc = parse_decimal(agente.get('km_excedente'))
        total = Decimal('0')
        if motivo == "Antenista":
            valor_hora = parse_decimal(prestador.get('valorh_antenista'))
            valor_km = parse_decimal(prestador.get('valorkm_antenista'))
            valor_fixo = parse_decimal(prestador.get('valor_antenista'))
            total = (hora_exc * valor_hora) + (km_exc * valor_km) + valor_fixo
        elif motivo == "Pronta Resposta Armado":
            valor_hora = parse_decimal(prestador.get('valorh_armado'))
            valor_km = parse_decimal(prestador.get('valorkm_armado'))
            valor_fixo = parse_decimal(prestador.get('valor_prontaresposta_armado'))
            total = (hora_exc * valor_hora) + (km_exc * valor_km) + valor_fixo
        elif motivo == "Pronta Resposta Desarmado":
            valor_hora = parse_decimal(prestador.get('valorh_desarmado'))
            valor_km = parse_decimal(prestador.get('valorkm_desarmado'))
            valor_fixo = parse_decimal(prestador.get('valor_prontaresposta_desarmado'))
            total = (hora_exc * valor_hora) + (km_exc * valor_km) + valor_fixo
        return total

    def calcular_total_cliente(cliente_data, agentes):
        total = Decimal('0')
        for agente in agentes:
            motivo = agente.get('motivo', '')
            km_total = parse_decimal(agente.get('km_total'))
            horas_decimais = diferenca_horas(agente.get('data_hora_inicial'), agente.get('data_hora_final'))
            if motivo == "Antenista":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_antenista')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_antenista')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_antenista'))
                val_hora = parse_decimal(cliente_data.get('valorh_antenista'))
                fixed_activation = parse_decimal(cliente_data.get('valor_antenista'))
            elif motivo == "Pronta Resposta Armado":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_armado')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_armado')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_armado'))
                val_hora = parse_decimal(cliente_data.get('valorh_armado'))
                fixed_activation = parse_decimal(cliente_data.get('valor_prontaresposta_armado'))
            elif motivo == "Pronta Resposta Desarmado":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_desarmado')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_desarmado')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_desarmado'))
                val_hora = parse_decimal(cliente_data.get('valorh_desarmado'))
                fixed_activation = parse_decimal(cliente_data.get('valor_prontaresposta_desarmado'))
            else:
                continue
            custo_excedente = (km_exced * val_km) + (hora_exced * val_hora)
            total += custo_excedente + fixed_activation
        return total

    def calcular_horas_cliente(agentes, cliente):
        hora_total_cliente = Decimal('0')
        hora_excedente_cliente = Decimal('0')
        for ag in agentes:
            horas_decimais = diferenca_horas(ag.get('data_hora_inicial'), ag.get('data_hora_final'))
            hora_total_cliente += horas_decimais
            franquia_hora_cliente = Decimal('0')
            motivo = ag.get('motivo', '')
            if motivo == "Antenista":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_antenista'))
            elif motivo == "Pronta Resposta Armado":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_armado'))
            elif motivo == "Pronta Resposta Desarmado":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_desarmado'))
            hora_exced = horas_decimais - franquia_hora_cliente
            if hora_exced < 0:
                hora_exced = Decimal('0')
            hora_excedente_cliente += hora_exced
        return str(hora_total_cliente), str(hora_excedente_cliente)

    registro = get_object_or_404(RegistroPagamento, pk=pk)
    cliente_data = {
        'nome': format_field(registro.cliente.nome),
        'cnpj': format_field(registro.cliente.cnpj),
        'telefone': format_field(registro.cliente.telefone),
        'banco': format_field(registro.cliente.banco),
        'agencia': format_field(registro.cliente.agencia),
        'conta': format_field(registro.cliente.conta),
        'servicos': format_field(registro.cliente.servicos),
        'valor_prontaresposta_armado': format_field(registro.cliente.valor_prontaresposta_armado),
        'franquia_hora_armado': format_field(registro.cliente.franquia_hora_armado),
        'franquia_km_armado': format_field(registro.cliente.franquia_km_armado),
        'valorkm_armado': format_field(registro.cliente.valorkm_armado),
        'valorh_armado': format_field(registro.cliente.valorh_armado),
        'valor_prontaresposta_desarmado': format_field(registro.cliente.valor_prontaresposta_desarmado),
        'franquia_hora_desarmado': format_field(registro.cliente.franquia_hora_desarmado),
        'franquia_km_desarmado': format_field(registro.cliente.franquia_km_desarmado),
        'valorkm_desarmado': format_field(registro.cliente.valorkm_desarmado),
        'valorh_desarmado': format_field(registro.cliente.valorh_desarmado),
        'valor_antenista': format_field(registro.cliente.valor_antenista),
        'franquia_hora_antenista': format_field(registro.cliente.franquia_hora_antenista),
        'franquia_km_antenista': format_field(registro.cliente.franquia_km_antenista),
        'valorkm_antenista': format_field(registro.cliente.valorkm_antenista),
        'valorh_antenista': format_field(registro.cliente.valorh_antenista),
    }
    # Agente principal
    agente_principal = {
        'id_prestador': registro.prestador.id if registro.prestador else None,
        'nome': format_field(registro.prestador.Nome if registro.prestador else None),
        'cpf_cnpj': format_field(registro.prestador.cpf_cnpj if registro.prestador else None),
        'telefone': format_field(registro.prestador.telefone if registro.prestador else None),
        'banco': format_field(registro.prestador.banco if registro.prestador else None),
        'agencia': format_field(registro.prestador.agencia if registro.prestador else None),
        'conta': format_field(registro.prestador.conta if registro.prestador else None),
        'servicos': format_field(registro.prestador.servicos if registro.prestador else None),
        'motivo': format_field(registro.motivo),
        'data_hora_inicial': format_datetime_field(registro.data_hora_inicial),
        'data_hora_final': format_datetime_field(registro.data_hora_final),
        'hora_excedente': str(registro.hora_excedente) if registro.hora_excedente is not None else "0",
        'hora_total': str(registro.hora_total) if registro.hora_total is not None else "0",
        'km_total': str(registro.km_total) if registro.km_total is not None else "0",
        'km_excedente': str(registro.km_excedente) if registro.km_excedente is not None else "0",
        'valor_prontaresposta_armado': format_field(registro.prestador.valor_prontaresposta_armado if registro.prestador else None),
        'franquia_hora_armado': format_field(registro.prestador.franquia_hora_armado if registro.prestador else None),
        'franquia_km_armado': format_field(registro.prestador.franquia_km_armado if registro.prestador else None),
        'valorkm_armado': format_field(registro.prestador.valorkm_armado if registro.prestador else None),
        'valorh_armado': format_field(registro.prestador.valorh_armado if registro.prestador else None),
        'valor_prontaresposta_desarmado': format_field(registro.prestador.valor_prontaresposta_desarmado if registro.prestador else None),
        'franquia_hora_desarmado': format_field(registro.prestador.franquia_hora_desarmado if registro.prestador else None),
        'franquia_km_desarmado': format_field(registro.prestador.franquia_km_desarmado if registro.prestador else None),
        'valorkm_desarmado': format_field(registro.prestador.valorkm_desarmado if registro.prestador else None),
        'valorh_desarmado': format_field(registro.prestador.valorh_desarmado if registro.prestador else None),
        'valor_antenista': format_field(registro.prestador.valor_antenista if registro.prestador else None),
        'franquia_hora_antenista': format_field(registro.prestador.franquia_hora_antenista if registro.prestador else None),
        'franquia_km_antenista': format_field(registro.prestador.franquia_km_antenista if registro.prestador else None),
        'valorkm_antenista': format_field(registro.prestador.valorkm_antenista if registro.prestador else None),
        'valorh_antenista': format_field(registro.prestador.valorh_antenista if registro.prestador else None),
        'id_acionamento': registro.id,
    }
    # Calcular total do agente principal
    agente_principal['total'] = float(calcular_total_agente(
        agente_principal['motivo'], agente_principal, agente_principal
    ))

    agentes_adicionais = []
    for idx, prestador in enumerate([registro.prestador1, registro.prestador2, registro.prestador3], start=1):
        if prestador:
            ag = {
                'id_acionamento': registro.id,  # Se cada adicional tiver um id diferente, ajuste aqui
                'id_prestador': prestador.id,
                'nome': format_field(prestador.Nome),
                'cpf_cnpj': format_field(prestador.cpf_cnpj),
                'telefone': format_field(prestador.telefone),
                'banco': format_field(prestador.banco),
                'agencia': format_field(prestador.agencia),
                'conta': format_field(prestador.conta),
                'servicos': format_field(prestador.servicos),
                'motivo': format_field(getattr(registro, f'motivo{idx}', None)),
                'data_hora_inicial': format_datetime_field(getattr(registro, f'data_hora_inicial{idx}', None)),
                'data_hora_final': format_datetime_field(getattr(registro, f'data_hora_final{idx}', None)),
                'hora_excedente': str(getattr(registro, f'hora_excedente{idx}', 0) or "0"),
                'hora_total': str(getattr(registro, f'hora_total{idx}', 0) or "0"),
                'km_total': str(getattr(registro, f'km_total{idx}', 0) or "0"),
                'km_excedente': str(getattr(registro, f'km_excedente{idx}', 0) or "0"),
                'valor_prontaresposta_armado': format_field(prestador.valor_prontaresposta_armado),
                'franquia_hora_armado': format_field(prestador.franquia_hora_armado),
                'franquia_km_armado': format_field(prestador.franquia_km_armado),
                'valorkm_armado': format_field(prestador.valorkm_armado),
                'valorh_armado': format_field(prestador.valorh_armado),
                'valor_prontaresposta_desarmado': format_field(prestador.valor_prontaresposta_desarmado),
                'franquia_hora_desarmado': format_field(prestador.franquia_hora_desarmado),
                'franquia_km_desarmado': format_field(prestador.franquia_km_desarmado),
                'valorkm_desarmado': format_field(prestador.valorkm_desarmado),
                'valorh_desarmado': format_field(prestador.valorh_desarmado),
                'valor_antenista': format_field(prestador.valor_antenista),
                'franquia_hora_antenista': format_field(prestador.franquia_hora_antenista),
                'franquia_km_antenista': format_field(prestador.franquia_km_antenista),
                'valorkm_antenista': format_field(prestador.valorkm_antenista),
                'valorh_antenista': format_field(prestador.valorh_antenista),
            }
            # Calcular total do agente adicional
            ag['total'] = float(calcular_total_agente(ag['motivo'], ag, ag))
            agentes_adicionais.append(ag)
    todos_agentes = [agente_principal] + agentes_adicionais
    total_cliente = calcular_total_cliente(cliente_data, todos_agentes)
    hora_total_cliente, hora_excedente_cliente = calcular_horas_cliente(todos_agentes, cliente_data)
    custo_agentes = sum([parse_decimal(str(ag.get('total', '0'))) for ag in todos_agentes])
    return JsonResponse({
        'cliente': cliente_data,
        'agente_principal': agente_principal,
        'agentes_adicionais': agentes_adicionais,
        'total_cliente': str(total_cliente),
        'hora_total_cliente': hora_total_cliente,
        'hora_excedente_cliente': hora_excedente_cliente,
        'custo_agentes': str(custo_agentes),
        'data_hora_inicial': agente_principal['data_hora_inicial'] or "—",
        'data_hora_final': agente_principal['data_hora_final'] or "—",
        'id_acionamento': registro.id,
    })

def faturar(request, pk):
    registro = get_object_or_404(RegistroPagamento, pk=pk)
    registro.status = "Faturado"
    registro.save()
    return redirect('formacompanhamento:registro_pagamento_list')  # ou onde preferir

class FaturamentoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = RegistroPagamento
    template_name = 'faturamento.html'
    context_object_name = 'registros'
    permission_required = "formacompanhamento.view_agentes"
    paginate_by = 10  # se quiser paginação

    def get_queryset(self):
        queryset = super().get_queryset()

        # Lê os valores digitados no formulário (GET)
        filtro_id = self.request.GET.get('id', '').strip()
        filtro_cliente = self.request.GET.get('cliente', '').strip()
        filtro_data_inicio = self.request.GET.get('data_inicio', '').strip()
        filtro_data_fim = self.request.GET.get('data_fim', '').strip()
        filtro_status = self.request.GET.get('status', '').strip()

        # 1) Filtra por ID (se for numérico)
        if filtro_id.isdigit():
            queryset = queryset.filter(id=filtro_id)

        # 2) Filtra por Cliente
        if filtro_cliente:
            queryset = queryset.filter(cliente__nome__icontains=filtro_cliente)

        # 3) Filtra por intervalo de data (Data/Hora Inicial)
        if filtro_data_inicio:
            queryset = queryset.filter(data_hora_inicial__date__gte=filtro_data_inicio)
        if filtro_data_fim:
            queryset = queryset.filter(data_hora_inicial__date__lte=filtro_data_fim)

        # 4) Filtra por Status (case-insensitive)
        # Se nenhum filtro for informado, por padrão, filtra para "A Faturar"
        if filtro_status:
            queryset = queryset.filter(status__iexact=filtro_status)
        else:
            queryset = queryset.filter(status__iexact="A Faturar")

        return queryset


    
def marcar_pago(request, pk):
    reg = get_object_or_404(RegistroPagamento, pk=pk)
    reg.status = "Pago"
    reg.save()
    return redirect('formacompanhamento:faturamento_lista') # ou outra rota que liste os registros






from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import prestadores

@require_GET
def all_prestadores_addresses(request):
    # Consulta todos os prestadores
    prestadores_list = prestadores.objects.all()
    
    # Cria uma lista de dicionários com os dados desejados
    data = []
    for p in prestadores_list:
        data.append({
            "id": p.pk,
            "nome": p.Nome,
            "latlong": p.lat_long,
        })
    
    return JsonResponse(data, safe=False)


# views.py

from django.shortcuts import render

def mapa_mapbox_view(request):
    # Captura o endereço que veio por GET
    endereco = request.GET.get("endereco", "")
    # Renderiza um template (ex: 'mapa_mapbox.html') com esse endereço
    return render(request, "mapa_mapbox.html", {"endereco": endereco})





from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import OcorrenciaTransporteForm
from .models import OcorrenciaTransporte

@login_required
def ocorrencia_transporte_create(request):
    if request.method == 'POST':
        form = OcorrenciaTransporteForm(request.POST)
        if form.is_valid():
            ocorrencia = form.save(commit=False)
            ocorrencia.usuario = request.user  # Sempre preenche o usuário logado
            ocorrencia.save()
            messages.success(request, 'Ocorrência registrada com sucesso!')
            return redirect('formacompanhamento:ocorrencia_transporte_list')
    else:
        form = OcorrenciaTransporteForm()
    return render(request, 'formacompanhamento/ocorrencia_transporte_form.html', {'form': form})

def ocorrencia_transporte_list(request):
    ocorrencias = OcorrenciaTransporte.objects.all().order_by('-data_hora_ocorrencia')
    return render(request, 'formacompanhamento/ocorrencia_transporte_list.html', {'ocorrencias': ocorrencias})

@login_required
def ocorrencia_transporte_update(request, pk):
    ocorrencia = get_object_or_404(OcorrenciaTransporte, pk=pk)
    if request.method == 'POST':
        form = OcorrenciaTransporteForm(request.POST, instance=ocorrencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ocorrência atualizada com sucesso!')
            return redirect('formacompanhamento:ocorrencia_transporte_list')
    else:
        form = OcorrenciaTransporteForm(instance=ocorrencia)
    return render(request, 'formacompanhamento/ocorrencia_transporte_form.html', {'form': form})

@login_required
def ocorrencia_transporte_delete(request, pk):
    ocorrencia = get_object_or_404(OcorrenciaTransporte, pk=pk)
    if request.method == 'POST':
        ocorrencia.delete()
        messages.success(request, 'Ocorrência excluída com sucesso!')
        return redirect('formacompanhamento:ocorrencia_transporte_list')
    return render(request, 'formacompanhamento/ocorrencia_transporte_confirm_delete.html', {'object': ocorrencia})

from django.views.decorators.http import require_GET
from django.http import JsonResponse
from .models import RegistroPagamento

@require_GET
def api_todos_acionamentos(request):
    from decimal import Decimal
    from django.utils.dateparse import parse_datetime
    from django.utils.timezone import is_naive, make_aware

    def format_field(value, default="Não informado"):
        return str(value) if value is not None else default

    def format_datetime_field(dt):
        if not dt:
            return ""
        if isinstance(dt, str):
            return dt
        try:
            if is_naive(dt):
                dt = make_aware(dt)
            return dt.isoformat()
        except Exception:
            return str(dt)

    def parse_decimal(value):
        if not value or value == "Não informado":
            return Decimal('0')
        try:
            return Decimal(str(value).replace(',', '.'))
        except Exception:
            return Decimal('0')

    def diferenca_horas(inicio, fim):
        if not inicio or not fim:
            return Decimal('0')
        try:
            if isinstance(inicio, str):
                inicio = parse_datetime(inicio)
            if isinstance(fim, str):
                fim = parse_datetime(fim)
            if not inicio or not fim:
                return Decimal('0')
            diff = fim - inicio
            return Decimal(str(diff.total_seconds() / 3600))
        except Exception:
            return Decimal('0')

    def calcular_total_cliente(cliente_data, agentes):
        total = Decimal('0')
        for agente in agentes:
            motivo = agente.get('motivo', '')
            km_total = parse_decimal(agente.get('km_total'))
            horas_decimais = diferenca_horas(agente.get('data_hora_inicial'), agente.get('data_hora_final'))
            if motivo == "Antenista":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_antenista')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_antenista')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_antenista'))
                val_hora = parse_decimal(cliente_data.get('valorh_antenista'))
                fixed_activation = parse_decimal(cliente_data.get('valor_antenista'))
            elif motivo == "Pronta Resposta Armado":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_armado')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_armado')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_armado'))
                val_hora = parse_decimal(cliente_data.get('valorh_armado'))
                fixed_activation = parse_decimal(cliente_data.get('valor_prontaresposta_armado'))
            elif motivo == "Pronta Resposta Desarmado":
                km_exced = max(km_total - parse_decimal(cliente_data.get('franquia_km_desarmado')), Decimal('0'))
                hora_exced = max(horas_decimais - parse_decimal(cliente_data.get('franquia_hora_desarmado')), Decimal('0'))
                val_km = parse_decimal(cliente_data.get('valorkm_desarmado'))
                val_hora = parse_decimal(cliente_data.get('valorh_desarmado'))
                fixed_activation = parse_decimal(cliente_data.get('valor_prontaresposta_desarmado'))
            else:
                continue
            custo_excedente = (km_exced * val_km) + (hora_exced * val_hora)
            total += custo_excedente + fixed_activation
        return str(total)

    def calcular_horas_cliente(agentes, cliente):
        hora_total_cliente = Decimal('0')
        hora_excedente_cliente = Decimal('0')
        for ag in agentes:
            horas_decimais = diferenca_horas(ag.get('data_hora_inicial'), ag.get('data_hora_final'))
            hora_total_cliente += horas_decimais
            franquia_hora_cliente = Decimal('0')
            motivo = ag.get('motivo', '')
            if motivo == "Antenista":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_antenista'))
            elif motivo == "Pronta Resposta Armado":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_armado'))
            elif motivo == "Pronta Resposta Desarmado":
                franquia_hora_cliente = parse_decimal(cliente.get('franquia_hora_desarmado'))
            hora_exced = horas_decimais - franquia_hora_cliente
            if hora_exced < 0:
                hora_exced = Decimal('0')
            hora_excedente_cliente += hora_exced
        return str(hora_total_cliente), str(hora_excedente_cliente)

    registros = RegistroPagamento.objects.all()
    resultado = []
    for registro in registros:
        if not registro.cliente:
            continue  # Skip records without a client
            
        cliente = registro.cliente
        cliente_data = {
            'id': cliente.id,
            'nome': format_field(cliente.nome),
            'cnpj': format_field(cliente.cnpj),
            'telefone': format_field(cliente.telefone),
            'banco': format_field(cliente.banco),
            'agencia': format_field(cliente.agencia),
            'conta': format_field(cliente.conta),
            'servicos': format_field(cliente.servicos),
            'valor_prontaresposta_armado': format_field(cliente.valor_prontaresposta_armado),
            'franquia_hora_armado': format_field(cliente.franquia_hora_armado),
            'franquia_km_armado': format_field(cliente.franquia_km_armado),
            'valorkm_armado': format_field(cliente.valorkm_armado),
            'valorh_armado': format_field(cliente.valorh_armado),
            'valor_prontaresposta_desarmado': format_field(cliente.valor_prontaresposta_desarmado),
            'franquia_hora_desarmado': format_field(cliente.franquia_hora_desarmado),
            'franquia_km_desarmado': format_field(cliente.franquia_km_desarmado),
            'valorkm_desarmado': format_field(cliente.valorkm_desarmado),
            'valorh_desarmado': format_field(cliente.valorh_desarmado),
            'valor_antenista': format_field(cliente.valor_antenista),
            'franquia_hora_antenista': format_field(cliente.franquia_hora_antenista),
            'franquia_km_antenista': format_field(cliente.franquia_km_antenista),
            'valorkm_antenista': format_field(cliente.valorkm_antenista),
            'valorh_antenista': format_field(cliente.valorh_antenista),
        }
        agente_principal = {
            'id_acionamento': registro.id,
            'id_prestador': registro.prestador.id if registro.prestador else None,
            'nome': format_field(registro.prestador.Nome if registro.prestador else None),
            'cpf_cnpj': format_field(registro.prestador.cpf_cnpj if registro.prestador else None),
            'telefone': format_field(registro.prestador.telefone if registro.prestador else None),
            'banco': format_field(registro.prestador.banco if registro.prestador else None),
            'agencia': format_field(registro.prestador.agencia if registro.prestador else None),
            'conta': format_field(registro.prestador.conta if registro.prestador else None),
            'servicos': format_field(registro.prestador.servicos if registro.prestador else None),
            'motivo': format_field(registro.motivo),
            'data_hora_inicial': format_datetime_field(registro.data_hora_inicial),
            'data_hora_final': format_datetime_field(registro.data_hora_final),
            'hora_excedente': str(registro.hora_excedente) if registro.hora_excedente is not None else "0",
            'hora_total': str(registro.hora_total) if registro.hora_total is not None else "0",
            'km_total': str(registro.km_total) if registro.km_total is not None else "0",
            'km_excedente': str(registro.km_excedente) if registro.km_excedente is not None else "0",
        }
        agentes_adicionais = []
        for idx, prestador in enumerate([registro.prestador1, registro.prestador2, registro.prestador3], start=1):
            if prestador:
                agentes_adicionais.append({
                    'id_acionamento': registro.id,
                    'id_prestador': prestador.id,
                    'nome': format_field(prestador.Nome),
                    'cpf_cnpj': format_field(prestador.cpf_cnpj),
                    'telefone': format_field(prestador.telefone),
                    'banco': format_field(prestador.banco),
                    'agencia': format_field(prestador.agencia),
                    'conta': format_field(prestador.conta),
                    'servicos': format_field(prestador.servicos),
                    'motivo': format_field(getattr(registro, f'motivo{idx}', None)),
                    'data_hora_inicial': format_datetime_field(getattr(registro, f'data_hora_inicial{idx}', None)),
                    'data_hora_final': format_datetime_field(getattr(registro, f'data_hora_final{idx}', None)),
                    'hora_excedente': str(getattr(registro, f'hora_excedente{idx}', 0) or "0"),
                    'hora_total': str(getattr(registro, f'hora_total{idx}', 0) or "0"),
                    'km_total': str(getattr(registro, f'km_total{idx}', 0) or "0"),
                    'km_excedente': str(getattr(registro, f'km_excedente{idx}', 0) or "0"),
                })
        todos_agentes = [agente_principal] + agentes_adicionais
        total_cliente = calcular_total_cliente(cliente_data, todos_agentes)
        hora_total_cliente, hora_excedente_cliente = calcular_horas_cliente(todos_agentes, cliente_data)
        # Imagens
        imagens = []
        for i in range(1, 46):
            img = getattr(registro, f'imagem{i}', None)
            if img:
                imagens.append(request.build_absolute_uri(img.url))
        resultado.append({
            'id_acionamento': registro.id,
            'cliente': cliente_data,
            'agente_principal': agente_principal,
            'agentes_adicionais': agentes_adicionais,
            'total_cliente': total_cliente,
            'hora_total_cliente': hora_total_cliente,
            'hora_excedente_cliente': hora_excedente_cliente,
            'status': registro.status,
            'data_hora_inicial': agente_principal['data_hora_inicial'],
            'data_hora_final': agente_principal['data_hora_final'],
            'imagens': imagens,
        })
    return JsonResponse({'acionamentos': resultado})




