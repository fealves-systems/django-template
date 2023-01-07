from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from accounts.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from accounts.forms.AccountsForm import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

def LoginUser(request):
    template_name = 'accounts/login.html'
    if request.method == 'POST':
        form = UserForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if (user is not None):
            login(request, user)
            return redirect(request.GET.get('next', '/tarefas/'))

        else:
            print("FORM LOGIN ERRORS -> ", form.errors)
            messages.error(request, "Usuario ou senha invalida")

    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, template_name, context)


def LogoutUser(request):
    logout(request)
    return redirect("accounts:login")

@login_required(login_url="/contas/login/")
def UserChangePassword(request):
    template_name = 'accounts/user_change_password.html'
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Senha atualizada com sucesso!")
        else:
            messages.error(request, "Não foi possível atualizar a senha do usuário!")
    form = PasswordChangeForm(user=request.user)
    context = {
        'form': form,
    }
    return render(request, template_name, context)


@login_required(login_url="/contas/login/")
def AddUser(request):
    print("add_user request:", request, request.user),
    template_name = 'accounts/add_user.html'
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            # this performs the hashing of the password
            f.set_password(f.password)
            f.save()
            messages.success(request, "Usuario adicionado com sucesso!")
    form = UserForm()
    context = {
        'form': form,
    }
    return render(request, template_name, context)
