from django.db import models
from .models_agentes import agentes 
 # Certifique-se de que o caminho está correto





from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

class clientes_acionamento(models.Model):
    servicos_options = [
        ("Antenista", "Antenista"),
        ("Ponta Resposta Armado", "Ponta Resposta Armado"),
        ("Pronta Resposta Desarmado", "Pronta Resposta Desarmado"),
        ("Todos os serviços", " Todos os servicos"),
    ]

    estados_br = [
        ("AC", "Acre"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("PA", "Pará"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("TO", "Tocantins"),
        ("AL", "Alagoas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("MA", "Maranhão"),
        ("PB", "Paraíba"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RN", "Rio Grande do Norte"),
        ("SE", "Sergipe"),
        ("DF", "Distrito Federal"),
        ("GO", "Goiás"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("ES", "Espírito Santo"),
        ("MG", "Minas Gerais"),
        ("RJ", "Rio de Janeiro"),
        ("SP", "São Paulo"),
        ("PR", "Paraná"),
        ("RS", "Rio Grande do Sul"),
        ("SC", "Santa Catarina"),
    ]

    nome = models.CharField(max_length=100, null=True, blank=True)
    cnpj = models.CharField(max_length=100, null=True, blank=True)
    telefone = models.CharField(max_length=100, null=True, blank=True)
    banco = models.CharField(max_length=100, null=True, blank=True)
    agencia = models.CharField(max_length=100, null=True, blank=True)
    conta = models.CharField(max_length=100, null=True, blank=True)

    servicos = models.CharField(
        choices=servicos_options,
        max_length=50,
        null=True,
        blank=True
    )

    valor_prontaresposta_armado = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_armado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    franquia_km_armado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorkm_armado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorh_armado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    valor_prontaresposta_desarmado = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_desarmado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    franquia_km_desarmado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorkm_desarmado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorh_desarmado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    valor_antenista = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_antenista = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    franquia_km_antenista = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorkm_antenista = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valorh_antenista = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    razao_social = models.CharField(max_length=100, null=True, blank=True)
    nome_fantasia = models.CharField(max_length=100, null=True, blank=True)
    inscricao_estadual = models.CharField(max_length=100, null=True, blank=True)
    inscricao_municipal = models.CharField(max_length=100, null=True, blank=True)
    atividade_principal = models.CharField(max_length=100, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(choices=estados_br, max_length=100, null=True, blank=True)
    
    representante_legal = models.CharField(max_length=100, null=True, blank=True)
    contato_legal = models.CharField(max_length=100, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=100, null=True, blank=True)
    email_legal = models.CharField(max_length=100, null=True, blank=True)
   
   
    representante_financeiro = models.CharField(max_length=100, null=True, blank=True)
    contato_financeiro = models.CharField(max_length=100, null=True, blank=True)
    email_financeiro = models.CharField(max_length=100, null=True, blank=True)
    
    representante_operacional = models.CharField(max_length=100, null=True, blank=True)
    contato_operacional = models.CharField(max_length=100, null=True, blank=True)
    email_operacional = models.CharField(max_length=100, null=True, blank=True)
    
    
    endereco = models.CharField(max_length=100, null=True, blank=True)
    cep = models.CharField(max_length=100, null=True, blank=True)
    dias_a_faturar = models.CharField(max_length=100, null=True, blank=True)

    data_de_fechamento = models.DateField(
        verbose_name="Data de Fechamento",
        blank=True,
        null=True,
        help_text="Informe a data de fechamento, se aplicável."
    )

    # CAMPOS PARA UPLOAD DE PDFs
    contrato_pdf = models.FileField(
        upload_to='contratos_pdf/',            # Ajuste o path se desejar
        validators=[FileExtensionValidator(['pdf'])],
        null=True,
        blank=True,
        help_text="Faça upload do PDF do Contrato, se houver."
    )
    proposta_pdf = models.FileField(
        upload_to='propostas_pdf/',            # Ajuste o path se desejar
        validators=[FileExtensionValidator(['pdf'])],
        null=True,
        blank=True,
        help_text="Faça upload do PDF da Proposta, se houver."
    )

    def __str__(self):
        return f"{self.nome or 'Cliente sem nome'} (ID: {self.id})"

class Formacompanhamento(models.Model):
    prestador2 = [
        ("Sombra armado", "Sombra armado")
    ]

    data_inicio = models.DateTimeField(blank=True, null=True)
    data_final = models.DateTimeField(blank=True, null=True)
    prestador = models.CharField(choices=prestador2, max_length=50, null=False, blank=False)
    agente = models.ForeignKey(agentes, on_delete=models.CASCADE)  # Usando 'agentes' com a primeira letra minúscula
    placa = models.CharField(max_length=255)
    id_equipamento = models.CharField(max_length=255)
    km_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    km_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pedagio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, null=True,blank=True, default='Pendente')

    def __str__(self):
        return self.placa

from django.db import models
from decimal import Decimal

from decimal import Decimal
from django.db import models

class Registro(models.Model):
    cliente = models.CharField(max_length=255)
    valor_acionamento = models.DecimalField(max_digits=10, decimal_places=2)
    valor_hora_excedente = models.DecimalField(max_digits=10, decimal_places=2)
    km_excedente = models.DecimalField(max_digits=10, decimal_places=2)
    valor_km_excedente = models.DecimalField(max_digits=10, decimal_places=2)
    acionamento = models.DecimalField(max_digits=10, decimal_places=2)
    total_cliente = models.DecimalField(max_digits=15, decimal_places=2)
    def __str__(self):
        return self.cliente 

    @classmethod
    def create_from_registro_pagamento(cls, registro_pagamento):
        return cls.objects.create(
            cliente=registro_pagamento.cliente,
            valor_acionamento=Decimal(registro_pagamento.valor_acionamento),
            valor_hora_excedente=Decimal(registro_pagamento.valor_hora_excedente),
            km_excedente=Decimal(registro_pagamento.km_excedente),
            valor_km_excedente=Decimal(registro_pagamento.valor_km_excedente),
            acionamento=Decimal(registro_pagamento.acionamento),
            total_cliente=Decimal(registro_pagamento.total_acionamento)
        )






from decimal import Decimal
from django.db import models
from .models import clientes_acionamento


class RegistroPagamento(models.Model):
    # Definição de campos do modelo
    cliente_choices = [
        ('Sompo', 'Sompo'),
    ]
   
    contato = [
        ('Whatsapp', 'Whatsapp'),
        ('E-mail', 'E-mail'),
        ('Telefone', 'Telefone'),
    ]
    services = [
        ('Roubo', 'Roubo'),
        ('Preservação', 'Preservação'),
        
    ]
    rastreador1 = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
    ]
    isca1 = [
        ('SIM', 'SIM'),
        ('NÃO', 'NÃO'),
    ]
    motivo_options = [
        ('Antenista', 'Antenista'),
        ('Pronta Resposta Armado', 'Pronta Resposta Armado'),
        ('Pronta Resposta Desarmado', 'Pronta Resposta Desarmado'),
        
    ]

    tipo_servicos = models.CharField(choices=services,max_length=50, null=True, blank=True)
    cliente = models.ForeignKey(clientes_acionamento, on_delete=models.SET_NULL, null=True,blank=True)
    motivo = models.CharField(choices=motivo_options,max_length=50, null=True, blank=True)
    motivo1 = models.CharField(choices=motivo_options,max_length=50, null=True, blank=True)
    motivo2 = models.CharField(choices=motivo_options,max_length=50, null=True, blank=True)
    motivo3 = models.CharField(choices=motivo_options,max_length=50, null=True, blank=True)
    data_hora_inicial = models.DateTimeField(null=True,blank=True)
    data_hora_inicial1 = models.DateTimeField(null=True,blank=True)
    data_hora_inicial2 = models.DateTimeField(null=True,blank=True)
    data_hora_inicial3 = models.DateTimeField(null=True,blank=True)
    data_hora_final = models.DateTimeField(null=True,blank=True)
    data_hora_final1 = models.DateTimeField(null=True,blank=True)
    data_hora_final2 = models.DateTimeField(null=True,blank=True)
    data_hora_final3 = models.DateTimeField(null=True,blank=True)
    data_hora_chegada = models.DateTimeField(null=True,blank=True)
    data_hora_chegada1 = models.DateTimeField(null=True,blank=True)
    data_hora_chegada2 = models.DateTimeField(null=True,blank=True)
    data_hora_chegada3 = models.DateTimeField(null=True,blank=True)
    prestador = models.ForeignKey('formacompanhamento.prestadores', on_delete=models.SET_NULL, related_name='prestadores',null=True,blank=True)
    prestador1 = models.ForeignKey('formacompanhamento.prestadores', on_delete=models.SET_NULL, related_name='prestadores1',null=True,blank=True)
    prestador2 = models.ForeignKey('formacompanhamento.prestadores', on_delete=models.SET_NULL, related_name='prestadores2',null=True,blank=True)
    prestador3 = models.ForeignKey('formacompanhamento.prestadores', on_delete=models.SET_NULL, related_name='prestadores3',null=True,blank=True)
    previsa_chegada = models.DateTimeField(null=True, blank=True)
    protocolo = models.CharField(max_length=100,null=True,blank=True)
    solicitante = models.CharField(max_length=100, null=True,blank=True)
    endereco = models.CharField(max_length=100, null=True,blank=True)
    tipo_contato = models.CharField(choices=contato, max_length=100, null=True,blank=True)
    operador = models.CharField(max_length=100,null=True,blank=True)
    modelo = models.CharField(max_length=100, null=True,blank=True)
    cor = models.CharField(max_length=100, null=True,blank=True)
    ano = models.CharField(max_length=100, null=True,blank=True)
    ultima_posicao = models.CharField(max_length=100, null=True, blank=True)
    ultima_posicao_isca = models.CharField(max_length=100, null=True, blank=True)
    id_isca = models.CharField(max_length=100, null=True, blank=True)
    latlong = models.CharField(max_length=100, null=True, blank=True)
    latlong_isca = models.CharField(max_length=100, null=True, blank=True)
    quantidade_agentes = models.PositiveIntegerField(null=True,blank=True)
    id_equipamento = models.CharField(max_length=50, null=True, blank=True)
    rastreador = models.CharField(choices=rastreador1, max_length=100, null=True,blank=True)
    isca = models.CharField(choices=isca1, max_length=100, null=True,blank=True)
    acionamento = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acionamento1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acionamento2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    acionamento3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    hora_total = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_total1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_total2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_total3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    franquia_hora = models.IntegerField(null=True,blank=True)
    franquia_hora1 = models.IntegerField(null=True,blank=True)
    franquia_hora2 = models.IntegerField(null=True,blank=True)
    franquia_hora3 = models.IntegerField(null=True,blank=True)
    valor_hora_excedente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_hora_excedente1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_hora_excedente2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_hora_excedente3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    placas1 = models.CharField(max_length=100,null=True,blank=True)
    placas2 = models.CharField(max_length=100,null=True,blank=True)
    placas3 = models.CharField(max_length=100,null=True,blank=True)
    agentes = models.IntegerField(null=True, blank=True)
    sla = models.DurationField(null=True, blank=True)
    hora_excedente = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_excedente1 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_excedente2 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    hora_excedente3 = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    km_inicial = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_inicial1 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_inicial2 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_inicial3 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_final = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_final1 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_final2 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_final3 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_total = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_total1 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_total2 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_total3 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_excedente = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_excedente1 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_excedente2 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_excedente3 = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    km_franquia = models.IntegerField(null=True,blank=True)
    km_franquia1 = models.IntegerField(null=True,blank=True)
    km_franquia2 = models.IntegerField(null=True,blank=True)
    km_franquia3 = models.IntegerField(null=True,blank=True)
    valor_km_excedente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_km_excedente1 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_km_excedente2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_km_excedente3 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valor_total_km_excedente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    pedagio = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    descricao = models.CharField(max_length=1000, null=True,blank=True)
    total_acionamento = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    status = models.CharField(max_length=50, default='Pendente', null=True,blank=True)
    imagem1 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem2 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem3 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem4 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem5 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem6 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem7 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem8 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem9 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem10 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem11 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem12 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem13 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem14 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem15 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem16 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem17 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem18 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem19 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem20 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem21 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem22 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem23 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem24 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem25 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem26 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem27 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem28 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem29 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem30 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem31 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem32 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem33 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem34 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem35 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem36 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem37 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem38 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem39 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem40 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem41 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem42 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem43 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem44 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    imagem45 = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)

    
    def calcular_hora_total(self):
        if self.data_hora_inicial and self.data_hora_final:
            delta = self.data_hora_final - self.data_hora_inicial
            return Decimal(delta.total_seconds()) / Decimal(3600)
        return Decimal('0.00')

    def calcular_km_total(self):
        try:
            return max(Decimal(self.km_final or 0) - Decimal(self.km_inicial or 0), Decimal('0.00'))
        except (TypeError, ValueError):
            return Decimal('0.00')

    def calcular_km_excedente(self):
        try:
            return max(self.calcular_km_total() - Decimal(self.km_franquia or 0), Decimal('0.00'))
        except (TypeError, ValueError):
            return Decimal('0.00')

    def calcular_valor_total_km_excedente(self):
        try:
            return round(self.calcular_km_excedente() * Decimal(self.valor_km_excedente or 0), 2)
        except (TypeError, ValueError):
            return Decimal('0.00')

    def calcular_hora_excedente(self):
        try:
            return max(self.calcular_hora_total() - Decimal(self.franquia_hora or 0), Decimal('0.00'))
        except (TypeError, ValueError):
            return Decimal('0.00')

    def calcular_valor_total_hora_excedente(self):
        try:
            return round(self.calcular_hora_excedente() * Decimal(self.valor_hora_excedente or 0), 2)
        except (TypeError, ValueError):
            return Decimal('0.00')

    def calcular_total_acionamento(self):
        try:
            return round(
                Decimal(self.acionamento or 0)
                + self.calcular_valor_total_hora_excedente()
                + self.calcular_valor_total_km_excedente()
                + Decimal(self.pedagio or 0),
                2,
            )
        except (TypeError, ValueError):
            return Decimal('0.00')

    # Sobrescrevendo o método save
    def save(self, *args, **kwargs):
        """Calcula e salva todos os campos derivados automaticamente."""
        # Calculando os valores antes de salvar
        self.hora_total = self.calcular_hora_total()
        self.km_total = self.calcular_km_total()
        self.km_excedente = self.calcular_km_excedente()
        self.valor_total_km_excedente = self.calcular_valor_total_km_excedente()
        self.hora_excedente = self.calcular_hora_excedente()
        self.total_acionamento = self.calcular_total_acionamento()
        
        # Salvando o registro
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"ID: {self.id} - Cliente: {self.cliente or 'N/A'}"





class Agente(models.Model):
    registro_pagamento = models.ForeignKey(RegistroPagamento, related_name='agentes2', on_delete=models.CASCADE)

    prestador = models.ForeignKey('formacompanhamento.prestadores', on_delete=models.CASCADE,related_name='prestadores05',null=True,blank=True)
    data_hora_inicial = models.DateTimeField()
    data_hora_chegada = models.DateTimeField(null=True, blank=True)
    data_hora_final = models.DateTimeField(null=True, blank=True)

    km_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    km_final = models.DecimalField(max_digits=10, decimal_places=2)
    km_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    km_excedente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    hora_excedente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    franquia_hora = models.DecimalField(max_digits=10, decimal_places=2)
    valor_hora_excedente = models.DecimalField(max_digits=10, decimal_places=2)
    km_franquia = models.DecimalField(max_digits=10, decimal_places=2)
    valor_km_excedente = models.DecimalField(max_digits=10, decimal_places=2)

    pedagio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Agente {self.id} para {self.registro_pagamento.protocolo}"







class prestadores(models.Model):
    status =[
        
        ("ATIVO","ATIVO"),
        ("INATIVO","INATIVO"),
        ("PENDENTE","PENDENTE"),
    ]
    servicos_options = [ 
                        
               
        ("Antenista","Antenista"),
        ("Ponta Resposta Armado","Ponta Resposta Armado"),
        ("Pronta Resposta Desarmado","Pronta Resposta Desarmado"),         
        ("Todos os serviços"," Todos os servicos"),         
        ("Antenista e Pronta Resposta Armado","Antenista e Pronta Resposta Armado"),         
        ("Antenista e Pronta Resposta Desrmado","Antenista e Pronta Resposta Desrmado"),         
               
                        
    ]
    estados_br = [
    ("AC", "Acre"),
    ("AP", "Amapá"),
    ("AM", "Amazonas"),
    ("PA", "Pará"),
    ("RO", "Rondônia"),
    ("RR", "Roraima"),
    ("TO", "Tocantins"),
    ("AL", "Alagoas"),
    ("BA", "Bahia"),
    ("CE", "Ceará"),
    ("MA", "Maranhão"),
    ("PB", "Paraíba"),
    ("PE", "Pernambuco"),
    ("PI", "Piauí"),
    ("RN", "Rio Grande do Norte"),
    ("SE", "Sergipe"),
    ("DF", "Distrito Federal"),
    ("GO", "Goiás"),
    ("MT", "Mato Grosso"),
    ("MS", "Mato Grosso do Sul"),
    ("ES", "Espírito Santo"),
    ("MG", "Minas Gerais"),
    ("RJ", "Rio de Janeiro"),
    ("SP", "São Paulo"),
    ("PR", "Paraná"),
    ("RS", "Rio Grande do Sul"),
    ("SC", "Santa Catarina"),
]

    
    
    
    Nome = models.CharField(max_length=50, null=True, blank=True)
    cpf_cnpj = models.CharField(max_length=50, null=True, blank=True)
    vencimento_cnh = models.DateField(null=True, blank=True)
    tipo_prestador = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.CharField(max_length=50, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True)
    estado = models.CharField(choices=estados_br ,max_length=50, null=True, blank=True)
    
    telefone = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    conta = models.CharField(max_length=50, null=True, blank=True)
    disponibilidade = models.CharField(max_length=50, null=True, blank=True)
    lat_long = models.CharField(max_length=50, null=True, blank=True)
    status_prestador = models.CharField(choices=status,max_length=50, null=True, blank=True)
    agencia= models.CharField(max_length=50, null=True, blank=True)
    tipo_de_conta= models.CharField(max_length=50, null=True, blank=True)
    banco= models.CharField(max_length=50, null=True, blank=True)
    
    
   
    franquia_km = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valor_acionamento = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    servicos = models.CharField(choices=servicos_options,max_length=50, null=True, blank=True)
    valor_prontaresposta_armado = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_armado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    franquia_km_armado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorkm_armado = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorh_armado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valor_prontaresposta_desarmado = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_desarmado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    franquia_km_desarmado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorkm_desarmado = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorh_desarmado  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valor_antenista = models.CharField(max_length=50, null=True, blank=True)
    franquia_hora_antenista  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    franquia_km_antenista  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorkm_antenista = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    valorh_antenista  = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    cnh = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    foto = models.ImageField(upload_to='imagens_registros/', null=True, blank=True)
    

    def __str__(self):
        # Retorna o nome do prestador. Pode adicionar mais informações, se necessário.
        return self.Nome






from django.db import models

class TotalRegistro(models.Model):
    registro_pagamento = models.ForeignKey('RegistroPagamento', on_delete=models.CASCADE)
    cliente = models.ForeignKey('clientes_acionamento', on_delete=models.CASCADE)
    total_acionamento = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    km_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    hora_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    franquia_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    franquia_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    valor_acionamento = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    valor_km = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    valor_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Registro {self.registro_pagamento} - Cliente {self.cliente}"



















class OcorrenciaTransporte(models.Model):
    TIPO_OCORRENCIA_CHOICES = [
        ('acidente', 'Acidente'),
        ('pane', 'Pane Mecânica'),
        ('roubo', 'Roubo/Furto'),
        ('atraso', 'Atraso'),
        ('outros', 'Outros'),
    ]

    transportadora = models.CharField(max_length=100, null=True, blank=True)
    placa = models.CharField(max_length=8, null=True, blank=True)
    carreta = models.CharField(max_length=8, null=True, blank=True)
    motorista = models.CharField(max_length=100, null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    local = models.CharField(max_length=255, null=True, blank=True)
    endereco = models.TextField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    longitude = models.DecimalField(max_digits=22, decimal_places=16, null=True, blank=True)
    tipo_ocorrencia = models.CharField(max_length=20, choices=TIPO_OCORRENCIA_CHOICES, null=True, blank=True)
    data_hora_ocorrencia = models.DateTimeField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Ocorrência de Transporte'
        verbose_name_plural = 'Ocorrências de Transporte'
        ordering = ['-data_hora_ocorrencia']

    def __str__(self):
        return f"Ocorrência {self.tipo_ocorrencia} - {self.placa} - {self.data_hora_ocorrencia}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.usuario:
            from realtime_notifications.tasks import create_notification
            tipo_ocorrencia_display = dict(self.TIPO_OCORRENCIA_CHOICES).get(self.tipo_ocorrencia, self.tipo_ocorrencia)
            title = f"Nova Ocorrência de Transporte - {tipo_ocorrencia_display}"
            message = f"""
            Transportadora: {self.transportadora}
            Placa: {self.placa}
            Motorista: {self.motorista}
            Local: {self.local}
            Tipo: {tipo_ocorrencia_display}
            Data/Hora: {self.data_hora_ocorrencia.strftime('%d/%m/%Y %H:%M') if self.data_hora_ocorrencia else 'Não informado'}
            """
            # Enviar notificação para todos os usuários
            for user in get_user_model().objects.all():
                create_notification.delay(user.id, title, message, self.id)


















