from django.db import models
from .TenantSystem import *


class Fone(models.Model):
    RESIDENCIAL = 'Residencial'
    CELULAR = 'Celular'
    WHATSAPP = 'WhatsApp'
    TRABALHO = 'Trabalho'
    OUTROS = 'Outros'
 
    FONE_OPCOES = [
        (RESIDENCIAL, 'Residencial'),
        (CELULAR, 'Celular'),
        (WHATSAPP, 'Whatsapp'),
        (TRABALHO, 'Trabalho'),
        (OUTROS, 'Outros')
    ]
    tipo_fone = models.CharField(
        max_length=15, choices=FONE_OPCOES, default=CELULAR)
    descricao = models.CharField(max_length=100, null=False, blank=True)
    numero = models.CharField(max_length=20, null=False)
    
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f"{self.id}: {self.tipo_fone} | {self.numero}"