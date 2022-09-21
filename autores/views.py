from django.http import Http404
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def register(request):

    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)

    return render(request, 'autores/pages/register.html', context={
        'form': form,
        'form_action': reverse("autores:register_validate")
    })


def register_validate(request):

    if not request.POST:
        raise Http404()

    register_form_data = request.POST
    request.session['register_form_data'] = register_form_data
    form = RegisterForm(register_form_data)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Usuário cadastrado com sucesso!')
        del(request.session['register_form_data'])

    return redirect('autores:register')


def login_view(request):

    form = LoginForm()

    return render(request, "autores/pages/login.html", context={
        'form': form,
        'form_action': reverse('autores:login_validate'),
    })

def login_validate(request):
    if not request.POST:
        raise Http404

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(request,
            username = form.cleaned_data.get('username'),
            password = form.cleaned_data.get('password')
        )

        if authenticated_user is not None:
            messages.success(request, "Login realizado com sucesso !")
            login(request, authenticated_user)

        else:
            messages.error(request, "Credenciais não autenticadas!")

    else:
        messages.error(request, "Nome de usuário ou senha inválidos, insira os campos novamente!")

    return redirect('autores:login')

@login_required(login_url='autores:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        raise Http404()

    if request.POST.get('username') != request.user.username:
        return redirect('autores:login')

    logout(request)
    return redirect('autores:login')