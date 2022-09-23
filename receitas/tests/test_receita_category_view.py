from django.urls import reverse , resolve
from receitas import views
from .test_receita_base import ReceitasTestBase

class CategoryViewTest(ReceitasTestBase):

    def test_receita_category_view_is_correct(self):
        resolver_object = resolve(reverse("receitas:category",kwargs={'category_id':2}))
        self.assertIs(resolver_object.func.view_class,views.ReceitaListViewCategory)

    def test_receita_category_view_status_code_is_404_if_not_receitas(self):
        response = self.client.get(reverse("receitas:category",kwargs={'category_id':1000}))
        self.assertEqual(response.status_code,404)

    def test_receita_category_view_loads_correct_template(self):
        self.make_receita()
        response = self.client.get(reverse("receitas:category",kwargs={'category_id':1}))
        self.assertTemplateUsed(response,'receitas/pages/category.html')

    def test_receita_category_template_dont_show_is_detail_false(self):
        receita = self.make_receita(is_published=False)
        response = self.client.get(reverse('receitas:category',kwargs={'category_id':receita.category.id}))
        self.assertEqual(response.status_code,404)


