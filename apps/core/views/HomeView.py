from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.forms import CategoryForm, TaskForm
from core.models import Category, Task


# Create your views here.
@login_required(login_url="/contas/login/")
def Homeview(request):
    return render(request, 'base.html', {})

@login_required(login_url="/contas/login/")
def HomeviewTest(request, id):
    context = {
        'id': id,
    }
    return render(request, 'base.html', context)


@login_required(login_url="/contas/login/")
def AddCategory(request):
    print("add_category request:", request, request.user),
    template_name = 'core/add_category.html'

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            messages.success(request, "Categoria adicionada com sucesso!")
    categories = Category.objects.filter(owner=request.user)
    form = CategoryForm()

    context = {
        'form': form,
        'categories': categories,
    }
    return render(request, template_name, context)

@login_required(login_url="/contas/login/")
def ListCategories(request):
    print("list_category request:", request, request.user),
    template_name = 'core/list_categories.html'
    categories = Category.objects.filter(owner=request.user)
    context = {
        'categories': categories,
    }
    return render(request, template_name, context)

@login_required(login_url="/contas/login/")
def EditCategory(request, id_category):
    print("edit_category request:", request, request.user),
    template_name = 'core/edit_category.html'
    category = get_object_or_404(Category, id=id_category, owner=request.user)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("tasks:list_categories")
    form = CategoryForm(instance=category)
    context = {
        'id_category': id_category,
        'form': form,
    }
    return render(request, template_name, context)


def DeleteCategory(request, id_category):
    category = Category.objects.get(id=id_category)
    if category.owner == request.user:
        category.delete()
    else:
        messages.error(request, 'Permissão negada!')

    return redirect('tasks:list_categories')


# ----------------------------------------------------------
@login_required(login_url="/contas/login/")
def AddTask(request):
    print("add_category request:", request, request.user),
    template_name = 'core/add_task.html'
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()
            form.save_m2m()  # To Save ManyToMany fields
            messages.success(request, "Tarefa adicionada com sucesso!")
        else:
            print(form.errors)
            messages.error(request, form.errors)

    form = TaskForm()
    tarefas = Task.objects.filter(owner=request.user)
    context = {
        'form': form,
        'tarefas': tarefas,
    }
    return render(request, template_name, context)

@login_required(login_url="/contas/login/")
def ListTasks(request):
    print("list_tasks request:", request, request.user),
    template_name = 'core/list_tasks.html'
    tasks = Task.objects.filter(owner=request.user).exclude(status='CD')
    context = {
        'tasks': tasks,
    }
    return render(request, template_name, context)

@login_required(login_url="/contas/login/")
def EditTask(request, id_task):
    print("edit_task request:", request, request.user),
    template_name = 'core/edit_task.html'
    task = get_object_or_404(Task, id=id_task, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("tasks:list_tasks")
    form = TaskForm(instance=task)
    context = {
        'id_task': id_task,
        'form': form,
    }
    return render(request, template_name, context)

@login_required(login_url="/contas/login/")
def DeleteTask(request, id_task):
    task = Task.objects.get(id=id_task)
    if task.owner == request.user:
        task.delete()
    else:
        messages.error(request, 'Permissão negada!')

    return redirect('tasks:list_tasks')
