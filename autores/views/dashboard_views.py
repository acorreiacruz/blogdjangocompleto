from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from autores.forms import EditRecipeForm
from receitas.models import Receitas
from django.http.response import Http404
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render, redirect


@method_decorator(
    login_required(login_url='autores:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardEditCreateRecipe(View):

    def return_render(self, form):
        return render(self.request, 'autores/pages/edit_recipe.html', context={
            'form': form,
        })

    def get_receita(self, id=None):
        receita = None

        if id is not None:
            receita = Receitas.objects.filter(
                id=id,
                author=self.request.user,
                is_published=False
            ).first()

            if not receita:
                raise Http404()

        return receita

    def get(self, request, pk=None):
        receita = self.get_receita(pk)
        form = EditRecipeForm(instance=receita)
        return self.return_render(form)


    def post(self, request, pk=None):

        receita = self.get_receita(pk)

        form = EditRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=receita
        )

        if form.is_valid():

            receita = form.save(commit=False)

            receita.author = request.user
            receita.is_published = False
            receita.preparation_step_is_html = False

            receita.save()

            messages.success(request, 'Receita editada com sucesso !')
            return redirect(
                reverse('autores:dashboard_edit_recipe',kwargs={'pk': receita.id})
            )

        return self.return_render(form)


class DashboardDeleteRecipe(DashboardEditCreateRecipe):

    def post(self, request):

        id = request.POST.get("id")
        receita = self.get_receita(id)

        receita.delete()

        messages.success(request, 'Receita excluída com sucesso !')
        return redirect('autores:dashboard')

