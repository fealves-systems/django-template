from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from cpf_field.models import CPFField
from .TenantSystem import *
from .Enderecos import *
from .Fones import *


class PerfilDoUsuario(models.Model):

    class Meta:
        verbose_name = "*Perfis dos Usuários"
        verbose_name_plural = "*Perfis dos Usuários"


    MASCULINO = 'Masculino'
    FEMININO = 'Feminino'
    OUTROS = 'Outros'
    SEXO_OPCOES = [
        ('1', 'Masculino'),
        ('2', 'Feminino'),
        ('3', 'Outros')
    ]

    ESTADO_CIVIL_OPCOES = [
        ('1', 'Casado(a)'),
        ('2', 'Solteiro(a)'),
        ('3', 'Divorciado(a)'),
        ('4', 'Viúvo(a)')
    ]

    TIPOPESSOA_OPCOES = [
        ('1', 'Administrador'),
        ('2', 'Cliente'),
        ('3', 'Colaborador(a)'),
        ('4', 'Parceiro(a), porém não-funcionário(a)')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_pessoa = models.CharField(max_length=1, choices=TIPOPESSOA_OPCOES, default=2)
    nome = models.CharField(max_length=100)
    cpf = CPFField(max_length=11)
    identidade = models.CharField(max_length=30,  blank=True, default="")
    sexo = models.CharField(max_length=15, choices=SEXO_OPCOES, default=MASCULINO)
    data_nascimento = models.CharField(max_length=10,  blank=True, default="")
    estado_civil = models.CharField(max_length=15, choices=ESTADO_CIVIL_OPCOES, default=2)
    conjuge = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    foto = models.ImageField(upload_to='pessoas_fotos/%Y/%m/%d/', null=True, blank=True)

    def foto_preview(self):

        from django.utils.html import escape
        if (self.foto):
            return mark_safe(u'<img src="%s" width="64" height="64"/>' % escape(self.foto.url))
        else:
            return mark_safe('<img src="" />')

    foto.short_description = 'Foto Preview'
    foto.allow_tags = True

    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE, null=True, blank=True)
    fones = models.ForeignKey(Fone, on_delete=models.CASCADE, null=True, blank=True)

    def fones_contato(self):

            clist =  ''
            for f in self.fones.all():
                clist += str(f)
                clist += "<br><br>"
       
            return mark_safe(clist)
    
    ativo = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    oper = models.IntegerField(default=0)
    tenant_system = models.ForeignKey(TenantSystem, on_delete=models.DO_NOTHING, default=1)

    def __str__(self):
        return f"{self.id}: {self.nome}, Aniversário: {self.data_nascimento} CPF: {self.cpf} Identidade:{self.identidade} Email:{self.email}  [Ativo:{self.ativo}]"



