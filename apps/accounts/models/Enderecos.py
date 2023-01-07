from django.db import models
from .TenantSystem import *


class Endereco(models.Model):
    RESIDENCIA = 'Residencial'
    TRABALHO = 'Trabalho'
    OUTROS = 'Outros'
    RAZAOSOCIAL = 'Razão Social'

    ENDERECO_OPCOES = [
        (RESIDENCIA, 'Residencia (PF)'),
        (TRABALHO, 'Trabalho (PF)'),
        (OUTROS, 'Outros (PF/PJ)'),
        (RAZAOSOCIAL, 'Razao Social (PJ)')
    ]
    tipo_endereco = models.CharField(
        max_length=15, choices=ENDERECO_OPCOES, default=RESIDENCIA)
    # models.ForeignKey(CepBROfficial, on_delete=models.DO_NOTHING, null=True)
    cep = models.CharField(max_length=8,  blank=True, default="")
    estado = models.CharField(max_length=2,  blank=True, default="")
    cidade = models.CharField(max_length=100,  blank=True, default="")
    bairro = models.CharField(max_length=100,  blank=True, default="")
    endereco = models.CharField(max_length=120, blank=True, default="")
    complemento = models.CharField(max_length=120, blank=True, default="")
    complemento2 = models.CharField(max_length=120, blank=True, default="")
    pais = models.CharField(max_length=25,  default='Brasil')
    ponto_referencia = models.CharField(max_length=120, blank=True, default="")
    observacao = models.CharField(max_length=255,  blank=True, default="")
    ativo = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f"{self.id}: {self.tipo_endereco} | {self.endereco} {self.complemento}, {self.bairro} | \
        {self.cidade}, {self.estado} - {self.pais}. Cep {self.cep}"
