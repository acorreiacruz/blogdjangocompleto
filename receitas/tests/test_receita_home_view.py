from django.urls import reverse , resolve
from receitas import views
from .test_receita_base import ReceitasTestBase

class HomeViewTest(ReceitasTestBase):

    def test_receita_home_view_is_correct(self):
        resolver_object = resolve(reverse('receitas:home'))
        self.assertIs(resolver_object.func.view_class, views.ReceitaListViewHome)

    def test_receita_home_view_status_code_is_200(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertEqual(response.status_code,200)

    def test_receita_home_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertTemplateUsed(response,'receitas/pages/home.html')

    def test_receita_home_template_loads_receitas(self):
        # Aqui precisa de uma receita
        self.make_receita()
        response = self.client.get(reverse('receitas:home'))
        response_content = response.content.decode('utf-8')
        self.assertIn('Título da Receita',response_content)

    def test_receita_home_template_dont_show_is_detail_false(self):
        self.make_receita(is_published=False)
        response = self.client.get(reverse('receitas:home'))
        self.assertIn("<h1>There is no recipe pusblished yet !</h1>",response.content.decode('utf-8'))

    def test_receita_home_template_show_no_recipe_found_is_not_receitas(self):
        response = self.client.get(reverse('receitas:home'))
        self.assertIn("<h1>There is no recipe pusblished yet !</h1>",response.content.decode('utf-8'))

    def test_receita_home_is_paginated(self):
        # Criando as receitas  para as paginações , 6 por página
        for i in range(18):
            kwargs = {'slug':f'slug-receita-{i}','author-data':{'username':f'u{i}'}}
            self.make_receita(**kwargs)
            response = self.client.get(reverse('receitas:home'))
            paginator_obj = response.context.get('receitas').paginator

            self.assertEquals(3,paginator_obj.num_pages)
