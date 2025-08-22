from django.db import models

# Create your models here.
class Esporadico(models.Model):
    nome_central = models.CharField(max_length=255)
    data_acionamento = models.DateTimeField(auto_now=True)
    km_inicial = models.IntegerField(null=True, blank=True)
    foto_inicial = models.ImageField(upload_to='fotos_esporadicos/', null=True, blank=True)
    km_final = models.IntegerField(null=True, blank=True)
    fotos_final = models.ImageField(upload_to='fotos_esporadicos/', null=True, blank=True)
    local_acionamento = models.CharField(max_length=255, null=True, blank=True)
    foto_local_acionamento = models.ImageField(upload_to='fotos_esporadicos/', null=True, blank=True)
    
    def __str__(self):
        return self.nome_central

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
