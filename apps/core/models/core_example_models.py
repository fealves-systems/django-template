from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField('Nome', max_length=150)
    description = models.TextField('Descricão', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}: {self.name}'


class Task(models.Model):
    PRIORITY_CHOICES = {
        ('B', 'Baixa'),
        ('M', 'Media'),
        ('A', 'Alta'),
    }
    STATUS_CHOICES = {
        ('EX', 'Em execucão'),
        ('PD', 'Pendente'),
        ('CD', 'Concluída'),
    }
    name = models.CharField('Tarefa', max_length=200)
    description = models.TextField('Descricão', blank=True, null=True)
    end_date = models.DateField(
        'Data Final', auto_now=False, auto_now_add=False)
    priority = models.CharField(
        'Prioridade', max_length=1, choices=PRIORITY_CHOICES)
    category = models.ManyToManyField(Category)
    status = models.CharField('Status', max_length=2, choices=STATUS_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}: {self.name}'
