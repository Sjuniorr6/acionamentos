# formacompanhamento/models_agentes.py
from django.db import models

class agentes(models.Model):
    agente = models.CharField(max_length=255, blank=True, null=True)
    placa = models.CharField(max_length=255, blank=True, null=True)
    franquia_hora = models.CharField(max_length=255, blank=True, null=True)
    franquia_km = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.agente 