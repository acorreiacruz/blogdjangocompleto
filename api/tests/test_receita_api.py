from unicodedata import category
from unittest.mock import patch
from django.urls import reverse
from parameterized import parameterized
from .test_api_mixin import APITestBase
from receitas.models import Receitas, Category


class ReceitaAPITest(APITestBase):
    def test_se_api_ao_listar_retorna_status_code_200(self):
        resposta = self.get_response()
        self.assertEqual(resposta.status_code, 200)

    @patch("api.views.PaginacaoCustomizada.page_size", 6)
    def test_se_api_ao_listar_retorna_o_numero_correto_por_pagina(self):
        # Criando 8 receitas
        receitas = self.make_recipe_set(8)
        # Listando as receitas
        resposta = self.get_response()
        # Verificando o número de receitas retornadas
        por_pagina = len(resposta.data.get("results"))
        self.assertEqual(por_pagina, 6)

    @patch("api.views.PaginacaoCustomizada.page_size", 6)
    def test_se_api_lista_por_categoria(self):
        author = self.make_author()
        categoria1 = self.make_category('categoria1')
        categoria2 = self.make_category('categoria2')
        receita1 = Receitas.objects.create(
            category=categoria1,
            author=author,
            title="Título da Receita da categoria 1",
            description="Descrição da Receita da categoria 1",
            slug="slug-da-receita-da-categoria-1",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=10,
            servings_unit="pessoas",
            preparation_step="Preparação da Receita",
            preparation_step_is_html=False,
            is_published=True
        )
        receita2 = Receitas.objects.create(
            category=categoria2,
            author=author,
            title="Título da Receita da categoria 2",
            description="Descrição da Receita da categoria 2",
            slug="slug-da-receita-da-categoria-2",
            preparation_time=10,
            preparation_time_unit="minutos",
            servings=10,
            servings_unit="pessoas",
            preparation_step="Preparação da Receita",
            preparation_step_is_html=False,
            is_published=True
        )
        resposta = self.get_response(query_params=f"?categoria={categoria1.id}")
        data = resposta.data.get('results')[0]
        self.assertEqual(resposta.data.get('count'), 1)
        self.assertEqual(receita1.title, data.get('title'))
        self.assertEqual(receita1.description, data.get('description'))
        self.assertEqual(receita1.slug, data.get('slug'))
        self.assertNotEqual(receita2.title, data.get('title'))
        self.assertNotEqual(receita2.description, data.get('description'))
        self.assertNotEqual(receita2.slug, data.get('slug'))


    def test_se_api_ao_detalhar_retorna_status_code_200(self):
        receita = self.make_receita()
        resposta = self.get_response(action="detail", pk=receita.id)
        self.assertEqual(resposta.status_code, 200)

    @parameterized.expand(
        [
            "id",
            "title",
            "description",
            "slug",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_step",
            "is_published",
        ]
    )
    def test_se_api_ao_detalhar_retorna_receita_correta(self, campo):
        receita = self.make_receita()
        resposta = self.get_response(action="detail", pk=receita.id)
        dados = resposta.data
        self.assertEqual(dados.get(campo), getattr(receita, campo))

    def test_se_api_ao_detalhar_retorna_status_code_404(self):
        resposta = self.get_response(action="detail", pk=1000)
        self.assertEqual(resposta.status_code, 404)

    def test_se_api_ao_criar_retorna_status_code_401(self):
        resposta = self.get_response(
            action="list", method="post", data=self.receita_data
        )
        self.assertEqual(resposta.status_code, 401)

    def test_se_api_ao_criar_retorna_status_code_201(self):
        tokens = self.get_tokens()
        resposta = self.get_response(
            action="list",
            method="post",
            data=self.receita_data,
            access=tokens.get("access"),
        )
        self.assertEqual(resposta.status_code, 201)

    @parameterized.expand(
        [
            "title",
            "description",
            "slug",
            "preparation_time",
            "preparation_time_unit",
            "servings",
            "servings_unit",
            "preparation_step",
            "is_published",
        ]
    )
    def test_se_api_cria_a_receita_de_forma_correta(self, campo):
        tokens = self.get_tokens()
        resposta = self.get_response(
            action="list",
            method="post",
            data=self.receita_data,
            access=tokens.get("access"),
        )
        self.assertEqual(resposta.data.get(campo), self.receita_data.get(campo))

    def test_se_api_ao_deletar_retorna_status_code_401(self):
        resposta = self.get_response(action="detail", method="delete", pk=3)
        self.assertEqual(resposta.status_code, 401)

    def test_se_api_ao_deletar_retorna_status_code_204(self):
        # Criando uma receita
        receita = self.make_receita()
        # Obtendo o access token
        resposta = self.client.post(
            reverse('api:token_obtain_pair'),
            data={
                'username':'username',
                'password':'qaz321'
            }
        )
        access = resposta.data.get('access')
        # Deletando a receita criada
        resposta = self.get_response(
            action="detail",
            method="delete",
            access=access,
            pk=receita.id,
        )
        self.assertEqual(resposta.status_code, 204)

    def test_se_api_ao_deletar_retorna_status_code_404(self):
        tokens = self.get_tokens()
        resposta = self.get_response(
            action="detail", method="delete", pk=1000, access=tokens.get("access")
        )
        self.assertEqual(resposta.status_code, 404)

    def test_se_api_ao_atulizar_retona_status_code_401(self):
        resposta = self.get_response(
            action="detail",
            method="patch",
            data={
                "title": "Este é o título da receita",
                "description": "Esta é a descrição da receita",
            },
            pk=100,
        )
        self.assertEqual(resposta.status_code, 401)

    def test_se_api_atualiza_a_receita(self):
        # Criando a receita a ser alterada
        receita = self.make_receita()
        # Obtendo os tokens
        resposta = self.client.post(
            reverse('api:token_obtain_pair'),
            data={
                'username':'username',
                'password':'qaz321'
            }
        )
        tokens = resposta.data
        # Atualizando a receita
        resposta = self.get_response(
            action="detail",
            method="patch",
            data={
                "title": "Título alterado KKKKKKKK",
                "slug": "titulo-alterado-kkkkkkkk",
                "description": "Descrição da receita alterada KKKKK",
            },
            access=tokens.get("access"),
            pk=receita.id,
        )

        # Obtendo a receita novamente
        resposta = self.get_response(action="detail", pk=receita.id)

        self.assertEqual(resposta.data.get("title"), "Título alterado KKKKKKKK")
        self.assertEqual(resposta.data.get("slug"), "titulo-alterado-kkkkkkkk")
        self.assertEqual(
            resposta.data.get("description"), "Descrição da receita alterada KKKKK"
        )

    def test_if_api_ao_atualizar_returna_status_code_200(self):
        receita = self.make_receita()
        resposta = self.client.post(
            reverse('api:token_obtain_pair'),
            data={
                'username':'username',
                'password':'qaz321'
            }
        )
        tokens = resposta.data
        # Atualizando a receita
        resposta = self.get_response(
            action="detail",
            method="patch",
            data={
                "title": "título alterado KKKKKKKK",
                "slug": "titulo-alterado-kkkkkkkk",
            },
            access=tokens.get("access"),
            pk=receita.id,
        )
        self.assertEqual(resposta.status_code, 200)

    def test_if_api_ao_atualizar_returna_status_code_404(self):
        tokens = self.get_tokens()
        resposta = self.get_response(
            action="detail",
            method="patch",
            data={"title": "Alguma coisa para o título"},
            access=tokens.get("access"),
            pk=1000,
        )
        self.assertEqual(resposta.status_code, 404)

    def test_se_api_bloqueia_um_usuario_deletar_uma_receita_que_nao_e_dele(self):
        # Criando o author que não é dono da receita
        author = self.make_author(
            "outro", "outro", "outrouser", "qaz321", "outrouser@email.com"
        )
        # Obtendo os tokens do usuário
        resposta = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "outrouser", "password": "qaz321"},
        )
        tokens = resposta.data
        # Criando a receita
        receita = self.make_receita()
        # Deletando a receita criada
        resposta = self.get_response(
            action="detail", method="delete", access=tokens.get("access"), pk=receita.id
        )

        self.assertEqual(resposta.status_code, 403)

    def test_se_api_bloqueia_um_usuario_alterar_uma_receita_que_nao_e_dele(self):
        # Criando o author que não é dono da receita
        author = self.make_author(
            "outro", "outro", "outrouser", "qaz321", "outrouser@email.com"
        )
        # Obtendo os tokens do usuário
        resposta = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "outrouser", "password": "qaz321"},
        )
        tokens = resposta.data
        # Criando a receita
        receita = self.make_receita()
        # Deletando a receita criada
        resposta = self.get_response(
            action="detail",
            method="patch",
            access=tokens.get("access"),
            pk=receita.id,
            data={
                "title": "Tentando alterar o título",
                "description": "Tentando alterar a descrição da receita kkkkkkkk",
            },
        )
        self.assertEqual(resposta.status_code, 403)
