from django.urls import reverse , resolve
from receitas import views
from .test_receita_base import ReceitasTestBase

class SearchViewTest(ReceitasTestBase):

    def test_receita_search_url_is_correct(self):
        url = reverse('receitas:search')
        self.assertEqual(url,'/receitas/search/')

    def test_receita_search_view_function_is_correct(self):
        resolver_object = resolve(reverse('receitas:search'))
        self.assertIs(resolver_object.func.view_class,views.ReceitaListViewSearch)

    def test_receita_search_view_loads_correct_template(self):
        response = self.client.get(reverse('receitas:search')+'?search=teste')
        self.assertTemplateUsed(response,'receitas/pages/search.html')

    def test_receita_search_view_return_satus_code_200_ok(self):
        response = self.client.get(reverse('receitas:search')+'?search=teste')
        self.assertEqual(response.status_code,200)

    def test_receita_search_retuns_404_if_no_input(self):
        url = f"{reverse('receitas:search')}"
        response = self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_receita_search_view_if_input_will_be_escaped(self):
        url = f"{reverse('receitas:search')}?search=teste"
        response = self.client.get(url)
        self.assertIn('Searching for &quot;teste&quot; Receitas',response.content.decode('utf-8'))

    def test_receita_search_can_find_by_title(self):

        url = reverse('receitas:search')
        title1 = 'Esta é a receita 1'
        title2 = 'Esta é a receita 2'

        receita1 = self.make_receita(
            title = title1,
            slug = 'slug-receita-1',
            author_data = {'username':'user1'}
        )

        receita2 = self.make_receita(
            title = title2,
            slug = 'slug-receita-2',
            author_data = {'username':'user2'}
        )

        response1 = self.client.get(f'{url}?search={title1}')
        response2 = self.client.get(f'{url}?search={title2}')
        response_both = self.client.get(f'{url}?search=esta')

        # Receita é passa para a view pelo context, esse é acessado no response pelo context, logo retorna uma QueryDict
        self.assertIn(receita1.title,response1.content.decode('utf-8'))
        self.assertIn(receita2.title,response2.content.decode('utf-8'))

        self.assertNotIn(receita1.title,response2.content.decode('utf-8'))
        self.assertNotIn(receita2.title,response1.content.decode('utf-8'))

        self.assertIn(receita1.title,response_both.content.decode('utf-8'))
        self.assertIn(receita2.title,response_both.content.decode('utf-8'))


