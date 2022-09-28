from django.test import TestCase
from receitas.models import Receitas,Category
from django.contrib.auth.models import User

# Classe que herda de TestCase e que se extende para ReceitasViewsTest, feita com o intuito de guardar as configurações para os teste, o setup e o teardown

class ReceitasTestBase(TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def make_category(self,name="Category"):
        return Category.objects.create(name = name)

    def make_author(
        self,
        first_name = "user",
        last_name = "name",
        username = "username",
        password = "qaz321",
        email = "username@email.com"
    ):


        return  User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            email = email)

    def make_receita(
        self,
        category_data = None,
        author_data = None,
        title = "Título da Receita",
        description = "Descrição da Receita",
        slug = "slug-da-receita",
        preparation_time = 10,
        preparation_time_unit = 'minutos',
        servings = 10,
        servings_unit = 'pessoas',
        preparation_step = 'Preparação da Receita',
        preparation_step_is_html = False,
        is_published = True
    ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Receitas.objects.create(
            category = self.make_category(**category_data),
            author = self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_step = preparation_step,
            preparation_step_is_html = preparation_step_is_html,
            is_published = is_published)

    def make_recipe_set(self,quant=10):
        recipes = []
        for i in range(0 , quant):
            title = f"Título da Receita-{i+1}"
            author_data = {
                'first_name': f'user{i+1}',
                'last_name': f'user{i+1}',
                'username': f"user{i+1}",
                'email': f"user{i+1}@email.com",
                'password': "Qaz321654"
            }
            recipe = self.make_receita(title=title, slug=None,author_data=author_data)
            recipes.append(recipe)
        return recipes