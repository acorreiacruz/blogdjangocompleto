from django.contrib.auth.models import User
from receitas.models import Receitas, Category
from django.urls import reverse
from rest_framework.test import APITestCase


class APITestBase(APITestCase):
    def __init__(self, *args, **kwargs):
        self.receita_data = {
            "title": "Título da Receita",
            "description": "Descrição da Receita",
            "slug": "slug-da-receita",
            "preparation_time": 10,
            "preparation_time_unit": "minutos",
            "servings": 10,
            "servings_unit": "pessoas",
            "preparation_step": "Preparação da Receita",
            "preparation_step_is_html": False,
            "is_published": True,
        }
        super().__init__(*args, **kwargs)

    def get_url(self, api="receitas", action="list", query_params='', **kwargs):
        url = reverse(f"api:{api}-api-{action}", kwargs={**kwargs}) + query_params
        return url

    def get_response(
        self,
        api="receitas",
        action="list",
        method="get",
        data=None,
        access=None,
        query_params='',
        **kwargs,
    ):
        if method == "get":
            resposta = self.client.get(
                self.get_url(api=api, action=action, query_params=query_params, **kwargs),
            )
        if method == "post":
            resposta = self.client.post(
                self.get_url(api=api, action=action, query_params=query_params, **kwargs),
                data=data,
                HTTP_AUTHORIZATION=f"Bearer {access}",
            )
        if method == "delete":
            resposta = self.client.delete(
                self.get_url(api=api, action=action, query_params=query_params, **kwargs),
                HTTP_AUTHORIZATION=f"Bearer {access}",
            )
        if method == "patch":
            resposta = self.client.patch(
                self.get_url(api=api, action=action, query_params=query_params, **kwargs),
                data=data,
                HTTP_AUTHORIZATION=f"Bearer {access}",
            )
        return resposta

    def get_tokens(self):
        author = self.make_author(username="user", password="qaz321")
        resposta = self.client.post(
            reverse("api:token_obtain_pair"),
            data={"username": "user", "password": "qaz321"},
        )
        return {
            "access": resposta.data.get("access"),
            "refresh": resposta.data.get("refresh")
        }

    def make_category(self, name="Category"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name="user",
        last_name="name",
        username="username",
        password="qaz321",
        email="username@email.com",
    ):

        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_receita(
        self,
        category_data=None,
        author_data=None,
        title="Título da Receita",
        description="Descrição da Receita",
        slug="slug-da-receita",
        preparation_time=10,
        preparation_time_unit="minutos",
        servings=10,
        servings_unit="pessoas",
        preparation_step="Preparação da Receita",
        preparation_step_is_html=False,
        is_published=True
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Receitas.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
        )

    def make_recipe_set(self, quant=10):
        recipes = []
        for i in range(0, quant):
            title = f"Título da Receita-{i+1}"
            author_data = {
                "first_name": f"user{i+1}",
                "last_name": f"user{i+1}",
                "username": f"user{i+1}",
                "email": f"user{i+1}@email.com",
                "password": "Qaz321654",
            }
            recipe = self.make_receita(title=title, slug=None, author_data=author_data)
            recipes.append(recipe)
        return recipes
