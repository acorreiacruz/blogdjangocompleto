from django.urls import reverse , resolve
from receitas import views
from .test_receita_base import ReceitasTestBase

class DetailViewTest(ReceitasTestBase):

    def test_receitas_detail_view_is_correct(self):
        resolver_object = resolve(reverse('receitas:receita',kwargs={'id':1}))
        self.assertIs(resolver_object.func,views.receita)
    
    def test_receita_detail_view_status_code_is_404_if_not_receitas(self):
        response = self.client.get(reverse('receitas:receita',kwargs={'id':100}))
        self.assertEqual(response.status_code,404)

    def test_receita_detail_view_loads_correct_template(self):
        self.make_receita()
        response = self.client.get(reverse('receitas:receita',kwargs={'id':1}))
        self.assertTemplateUsed(response,'receitas/pages/receita-view.html')

    def test_receita_detail_template_dont_show_is_detail_false(self):
        receita = self.make_receita(is_published=False)
        response = self.client.get(reverse('receitas:receita',kwargs={'id': receita.id}))
        self.assertEqual(response.status_code,404)


   