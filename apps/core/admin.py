from django.contrib import admin
from .models.core_example_models import *

admin.site.register(Category)
admin.site.register(Task)