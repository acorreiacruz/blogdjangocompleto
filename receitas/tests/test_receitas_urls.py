from django.test import TestCase
from django.urls import reverse

# Para criar um teste você deve declarar uma classe que herda de TestCase

class ReceitasUrlsTest(TestCase):
    def test_primeiro_funcionando(self):
        assert 1 == 1
    
    def test_receitas_home_url_is_correct(self):
        home_url = reverse('receitas:home')
        assert home_url == '/'

    def test_receitas_category_url_is_correct(self):
        category_url = reverse('receitas:category', kwargs={'category_id': 2})
        assert category_url == '/receitas/category/2/'

    def test_receitas_receita_detail_url_correct(self):
        detail_receita = reverse('receitas:receita',kwargs={'id':5})
        assert detail_receita == '/receitas/5/'

    def test_receita_search_url_is_correct(self):
        url = reverse('receitas:search')
        self.assertEqual(url,'/receitas/search/')