from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Esporadico(models.Model):
    nome_central = models.CharField(max_length=255)
    data_acionamento = models.DateTimeField(auto_now=True)
    km_inicial = models.IntegerField(null=True, blank=True)
    foto_inicial = models.ImageField(upload_to='fotos_esporadicos/', null=True, blank=True)
    km_final = models.IntegerField(null=True, blank=True)
    local_acionamento = models.CharField(max_length=255, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Criado por', related_name='esporadicos_criados', null=True, blank=True)
    
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
