from django.http import Http404
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm, EditRecipeForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from receitas.models import Receitas
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


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
        return redirect('autores:login')

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
            username = form.cleaned_data.get('username', ''),
            password = form.cleaned_data.get('password', '')
        )

        if authenticated_user is not None:
            messages.success(request, "Login realizado com sucesso !")
            login(request, authenticated_user)
            return redirect('autores:dashboard')

        else:
            messages.error(request, "Senha ou nome de usuário inválidos !")

    else:
        messages.error(request, "Nome de usuário ou senha inválidos, preencha os campos de forma correta !")

    return redirect('autores:login')


@login_required(login_url='autores:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        raise Http404()

    if request.POST.get('username') != request.user.username:
        return redirect('autores:login')

    logout(request)
    return redirect('autores:login')


@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard(request):
    receitas = Receitas.objects.filter(
        is_published=False,
        author=request.user
    )
    return render(request, 'autores/pages/dashboard.html', context={
        'receitas': receitas
    })


@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_edit_recipe(request, pk):

    receita = Receitas.objects.get(
        id=pk,
        author=request.user,
        is_published=False
    )

    form = EditRecipeForm(
        data=request.POST or None,
        instance=receita,
        files=request.FILES or None
    )

    if form.is_valid():

        receita = form.save(commit=False)

        receita.author = request.user
        receita.is_published = False
        receita.preparation_step_is_html = False

        receita.save()

        messages.success(request, 'Receita editada com sucesso !')
        return redirect(reverse('autores:dashboard_edit_recipe',kwargs={'pk':pk}))


    return render(request, 'autores/pages/edit_recipe.html', context={
        'id': pk,
        'form': form,
        'form_action': reverse('autores:dashboard_edit_recipe',kwargs={'pk':pk})
    })


@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_create_recipe(request):

    form = EditRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )

    if form.is_valid():
        receita = form.save(commit=False)

        receita.author = request.user
        receita.is_published = False
        receita.preparation_step_is_html = False

        receita.save()

        messages.success(request, 'Receita criada com sucesso !')
        return redirect('autores:dashboard')

    return render(request, 'autores/pages/edit_recipe.html', context={
        'form': form,
        'form_action': reverse('autores:dashboard_create_recipe')
    })


@login_required(login_url='autores:login', redirect_field_name='next')
def dashboard_delete_recipe(request):

    if request.method != 'POST':
        return Http404()

    id = request.POST.get("id")

    receita = get_object_or_404(
        Receitas.objects,
        id=id,
        author=request.user,
        is_published=False
    )

    receita.delete()
    messages.success(request, 'Receita excluída com sucesso !')
    return redirect('autores:dashboard')