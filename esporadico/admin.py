from django.contrib import admin
from .models import Esporadico, FotoEsporadico
from .forms import EsporadicoCreateForm, EsporadicoUpdateForm

@admin.register(Esporadico)
class EsporadicoAdmin(admin.ModelAdmin):
    list_display = ['nome_central', 'data_acionamento', 'km_inicial', 'km_final', 'local_acionamento', 'criado_por', 'valor_atribuido', 'valor_calculado']
    list_filter = ['data_acionamento', 'nome_central', 'criado_por']
    search_fields = ['nome_central', 'local_acionamento', 'criado_por__username']
    readonly_fields = ['data_acionamento', 'criado_por']
    ordering = ['-data_acionamento']
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:  # Criando um novo objeto
            self.form = EsporadicoCreateForm
        else:  # Editando um objeto existente
            self.form = EsporadicoUpdateForm
        return super().get_form(request, obj, **kwargs)
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_central', 'data_acionamento', 'criado_por')
        }),
        ('Quilometragem', {
            'fields': ('km_inicial', 'km_final')
        }),
        ('Horários', {
            'fields': ('hora_inicial', 'hora_final')
        }),
        ('Localização', {
            'fields': ('local_acionamento',)
        }),
        ('Documentação', {
            'fields': ('foto_inicial',)
        }),
        ('Valor', {
            'fields': ('valor_atribuido', 'valor_calculado')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editando um objeto existente
            return self.readonly_fields + ('data_acionamento',)
        return self.readonly_fields

class FotoEsporadicoInline(admin.TabularInline):
    model = FotoEsporadico
    extra = 1
    fields = ['foto', 'descricao']
    readonly_fields = ['data_upload']

# Adicionar inline ao EsporadicoAdmin
EsporadicoAdmin.inlines = [FotoEsporadicoInline]

@admin.register(FotoEsporadico)
class FotoEsporadicoAdmin(admin.ModelAdmin):
    list_display = ['esporadico', 'descricao', 'data_upload']
    list_filter = ['data_upload', 'esporadico__nome_central']
    search_fields = ['esporadico__nome_central', 'descricao']
    readonly_fields = ['data_upload']
    ordering = ['-data_upload']
