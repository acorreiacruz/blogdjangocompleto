from rest_framework.test import APITestCase
from django.urls import reverse
from parameterized import parameterized
from .test_api_mixin import APITestMixin


class ReceitaAPITest(APITestCase, APITestMixin):

    def test_se_api_list_retorna_status_code_200(self):
        url = reverse('api:receita-api-list')
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 200)

    def test_se_api_list_retorna_o_numero_correto_de_paginas(self):
        ...

    def test_se_api_list_retorna_o_numero_correto_por_pagina(self):
        ...

    def test_se_api_detail_retorna_status_code_200(self):
        url = reverse('api:receita-api-detail', kwargs={'id':1})
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 200)

    def test_se_api_detail_retorna_status_code_404(self):
        url = reverse('api:receita-api-detail', kwargs={'id':1})
        resposta = self.client.get(url)
        self.assertEqual(resposta.status_code, 404)

    def test_se_api_delete_retorna_status_code_201(self):
        ...

    def test_se_api_delete_retorna_status_code_404(self):
        ...

    @parameterized.expand(['list','detail','create','delete'])
    def test_se_api_retorna_status_code_401(self, action):
        resposta = self.client.get(
            reverse(f'api:receitas-api-{action}')
        )
        self.assertEqual(resposta.status_code, 402)