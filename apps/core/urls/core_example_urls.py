from django.urls import path
from core.views import *

app_name = "core" 

urlpatterns = [
    path("", Homeview, name="root"),
    path("test/<int:id>", HomeviewTest, name="test"),
    path("categorias/adicionar/", AddCategory, name="add_category"),
    path("categorias/editar/<int:id_category>", EditCategory, name="edit_category"),
    path("categorias/deletar/<int:id_category>", DeleteCategory, name="delete_category"),
    path("categorias/listar/", ListCategories, name="list_categories"),
    path("adicionar/", AddTask, name="add_task"),
    path("listar/", ListTasks, name="list_tasks"),
    path("editar/<int:id_task>", EditTask, name="edit_task"),
    path("deletar/<int:id_task>", DeleteTask, name="delete_task"),
]
