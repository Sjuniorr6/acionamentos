from django.contrib import admin
from .models import Formacompanhamento, RegistroPagamento, Registro

# Configuração para Formacompanhamento
class FormacompanhamentoAdmin(admin.ModelAdmin):
    list_display = (
        'data_inicio', 'data_final', 'prestador', 'agente',
        'placa', 'id_equipamento', 'km_inicial', 'km_final', 'pedagio'
    )
    search_fields = ('prestador', 'placa', 'id_equipamento')
    list_filter = ('data_inicio', 'data_final')

# Configuração para RegistroPagamento
class RegistroPagamentoAdmin(admin.ModelAdmin):
    list_display = (
        'cliente', 'data_hora_inicial', 'data_hora_final', 'prestador',
        'protocolo', 'solicitante',  'status', 'hora_total',
        'km_total', 'valor_total_km_excedente', 'total_acionamento', 'hora_excedente'  # Campo adicionado
    )
    search_fields = ('prestador', 'cliente', 'protocolo')
    list_filter = ('status', 'data_hora_inicial', 'data_hora_final')

    # Exibir total_acionamento formatado (opcional)
    def total_acionamento(self, obj):
        return f"{obj.total_acionamento:.2f}" if obj.total_acionamento else "0.00"
    total_acionamento.short_description = "Total Acionamento"

# Configuração para Registro
class RegistroAdmin(admin.ModelAdmin):
    list_display = (
        'cliente', 'hora_excedente', 'valor_hora_excedente',
        'km_excedente', 'valor_km_excedente', 'acionamento', 'total_cliente'
    )
    search_fields = ('cliente',)
    list_filter = ('cliente',)

    # Definindo 'hora_excedente' como um método
    def hora_excedente(self, obj):
        # Lógica para calcular ou retornar a hora excedente
        # Substitua pela lógica adequada, se necessário
        return obj.hora_excedente if hasattr(obj, 'hora_excedente') else "N/A"
    hora_excedente.short_description = "Hora Excedente"

# Registro no Django Admin
admin.site.register(Formacompanhamento, FormacompanhamentoAdmin)
admin.site.register(RegistroPagamento, RegistroPagamentoAdmin)
admin.site.register(Registro, RegistroAdmin)
