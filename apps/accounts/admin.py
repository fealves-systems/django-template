from django.contrib import admin
from .models.PerfisUsuarios import *

# Register your models here.
admin.site.register(TenantSystem)
admin.site.register(PerfilDoUsuario)
admin.site.register(Endereco)
admin.site.register(Fone)