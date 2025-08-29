from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.
class Esporadico(models.Model):
    nome_central = models.CharField(max_length=255)
    data_acionamento = models.DateTimeField(auto_now_add=True, verbose_name='Data e Hora do Acionamento')
    km_inicial = models.IntegerField(null=True, blank=True)
    foto_inicial = models.ImageField(upload_to='fotos_esporadicos/', null=True, blank=True)
    km_final = models.IntegerField(null=True, blank=True)
    local_acionamento = models.CharField(max_length=255, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criado por', related_name='esporadicos_criados', null=True, blank=True)
    hora_inicial = models.TimeField(null=True, blank=True, verbose_name='Hora Inicial')
    hora_final = models.TimeField(null=True, blank=True, verbose_name='Hora Final')
    valor_atribuido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Valor Atribuído')
    valor_calculado = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name='Valor Calculado')
    
    class Meta:
        verbose_name = 'Acionamento Esporádico'
        verbose_name_plural = 'Acionamentos Esporádicos'
        ordering = ['-data_acionamento']
    
    def __str__(self):
        return self.nome_central
    
    def total_fotos(self):
        """Retorna o total de fotos (inicial + adicionais)"""
        total = 0
        if self.foto_inicial:
            total += 1
        total += self.fotos_adicionais.count()
        return total
    
    def diferenca_horas(self):
        """Calcula a diferença em horas entre hora_final e hora_inicial"""
        if self.hora_inicial and self.hora_final:
            # Usar datetime.now() para data local
            base_date = datetime.now().date()
            inicio = datetime.combine(base_date, self.hora_inicial)
            fim = datetime.combine(base_date, self.hora_final)
            
            # Se a hora final for menor que a inicial, assumir que passou para o dia seguinte
            if fim < inicio:
                fim += timedelta(days=1)
            
            diferenca = fim - inicio
            return round(diferenca.total_seconds() / 3600, 2)  # Retorna em horas com 2 casas decimais
        return 0
    
    def diferenca_km(self):
        """Calcula a diferença em KM entre km_final e km_inicial"""
        if self.km_inicial and self.km_final:
            return self.km_final - self.km_inicial
        return 0
    
    def calcular_valor_total(self):
        """Calcula o valor total: valor_atribuido × diferenca_horas × diferenca_km"""
        if self.valor_atribuido:
            return self.valor_atribuido * self.diferenca_horas() * self.diferenca_km()
        return 0
    
    def save(self, *args, **kwargs):
        """Sobrescreve o método save para calcular automaticamente o valor_calculado"""
        if self.valor_atribuido:
            self.valor_calculado = self.calcular_valor_total()
        super().save(*args, **kwargs)

class FotoEsporadico(models.Model):
    esporadico = models.ForeignKey(Esporadico, on_delete=models.CASCADE, related_name='fotos_adicionais')
    foto = models.ImageField(upload_to='fotos_esporadicos/adicionais/')
    descricao = models.CharField(max_length=255, blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Foto Adicional'
        verbose_name_plural = 'Fotos Adicionais'
        ordering = ['data_upload']
    
    def __str__(self):
        return f"Foto {self.id} - {self.esporadico.nome_central}"
