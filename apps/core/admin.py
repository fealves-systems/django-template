from django.contrib import admin
from .models.tarefas import *

admin.site.register(Category)
admin.site.register(Task)