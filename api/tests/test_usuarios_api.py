from django.urls import reverse
from .test_api_mixin import APITestBase


class UsuariosAPITest(APITestBase):
    def test_se_api_retorna_ao_listar_status_code_401(self):
        resposta = self.get_response(api="usuarios")
        self.assertEqual(resposta.status_code, 401)

    def test_se_api_retorna_ao_listar_status_code_200(self):
        # Criando um usuário
        author = self.make_author()
        # Obtendo os tokens
        tokens = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "username", "password": "qaz321"},
        )
        access = tokens.data.get("access")

        # Realizando uma requisição para a url api/me/
        resposta = self.client.get(
            reverse("api:usuarios-api-list"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )
        self.assertEqual(resposta.status_code, 200)

    def test_se_api_me_retorna_status_code_200(self):
        # Criando um usuário
        author = self.make_author()
        # Obtendo os tokens
        tokens = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "username", "password": "qaz321"},
        )
        access = tokens.data.get("access")

        # Realizando uma requisição para a url api/me/
        resposta = self.client.get(
            reverse("api:usuarios-api-me"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )
        self.assertEqual(resposta.status_code, 200)

    def test_se_api_me_retorna_usuario_correto(self):
        # Criando um usuário
        author = self.make_author()
        # Obtendo os tokens
        tokens = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "username", "password": "qaz321"},
        )
        access = tokens.data.get("access")

        # Realizando uma requisição para a url api/me/
        resposta = self.client.get(
            reverse("api:usuarios-api-me"), HTTP_AUTHORIZATION=f"Bearer {access}"
        )
        self.assertEqual(resposta.data.get("id"), author.id)
        self.assertEqual(resposta.data.get("username"), author.username)
        self.assertEqual(resposta.data.get("email"), author.email)
