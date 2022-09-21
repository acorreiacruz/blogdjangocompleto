from .test_base_mixin import TestBaseMixin
from unittest import TestCase
from parameterized import parameterized
from autores.forms import LoginForm


class LoginFormUnitTest(TestCase):

    @parameterized.expand([
        ('password','Senha'),
        ('username', 'Nome de Usuário')
    ])
    def test_if_fields_label_is_correct(self, field, label):
        form = LoginForm()
        label_test = form[field].field.label
        self.assertEqual(label_test, label)

    @parameterized.expand([
        ('username','Digite o seu nome de usuário'),
        ('password','Insira a sua senha já cadastrada'),
    ])
    def test_if_fields_help_text_is_correct(self, field, help_text):
        form = LoginForm()
        help_text_test = form[field].field.help_text
        self.assertEqual(help_text_test, help_text)


    @parameterized.expand([
        ('username','Ex.: antoniocorreia'),
        ('password','Insira sua senha'),
    ])
    def test_if_fields_placeholder_is_correct(self, field, placeholder):
        form = LoginForm()
        placeholder_test = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, placeholder_test)


    @parameterized.expand([
        ('username','O campo de nome de usuário não pode ficar vazio!'),
        ('password','O campo de senha não pode ficar vazio!')
    ])
    def test_if_fields_error_messages_required_is_correct(self, field, required):
        form = LoginForm()
        required_test = form[field].field.error_messages['required']
        self.assertEqual(required_test, required)


class LoginFormIntegrationTest(TestBaseMixin):

    def setUp(self) -> None:
        self.form_data_register = {
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'username': 'jhondoe',
            'email': 'jhondoe@email.com',
            'password': 'P@as1234',
            'password_confirmation': 'P@as1234'
        }

        self.form_data_login = {
            'username': 'jhondoe',
            'password': 'P@as1234'
        }
        return super().setUp()

    @parameterized.expand([
        'Nome de Usuário',
        'Senha'
    ])
    def test_if_field_label_is_being_render_on_template(self,label):
        response = self.get_response('login')
        content = response.content.decode('utf-8')
        self.assertIn(label, content)

    @parameterized.expand([
        'Ex.: antoniocorreia',
        'Insira sua senha'
    ])
    def test_if_field_placeholder_is_being_render_on_template(self, placeholder):
        response = self.get_response('login')
        content = response.content.decode('utf-8')
        self.assertIn(placeholder, content)

    @parameterized.expand([
        'Digite o seu nome de usuário',
        'Insira a sua senha já cadastrada'
    ])
    def test_if_field_help_text_is_being_render_on_template(self, help_text):
        response = self.get_response('login')
        content = response.content.decode('utf-8')
        self.assertIn(help_text, content)

    def test_if_login_view_raise_404_on_get_method(self):
        response = self.get_response('login_validate')
        self.assertEqual(response.status_code, 404)

    def test_of_not_login_of_a_not_registered_user(self):
        response = self.client.login(**self.form_data_login)
        self.assertFalse(response)

    def test_login_of_registered_user(self):
        # Criando um usuário
        self.get_response('register_validate', 'post', self.form_data_register)

        # Realizando o login do usuário criado
        response = self.client.login(**self.form_data_login)
        self.assertTrue(response)

    def test_of_not_login_if_username_is_incorrect(self):
        # Criando um usuário
        self.get_response('register_validate', 'post', self.form_data_register)

        # Alterando o nome de usuário
        self.form_data_login['username'] = 'jhondoealter'

        # Tentar realizar o login do usuário com o nome de usuário errado
        response = self.client.login(**self.form_data_login)
        self.assertFalse(response)

    def test_of_not_login_if_password_is_incorrect(self):
        # Criando um usuário
        self.get_response('register_validate', 'post', self.form_data_register)

        # Alterando a senha
        self.form_data_login['password'] = 'Qaz321654'

        # Tentar realizar o login do usuário com a senha errada
        response = self.client.login(**self.form_data_login)
        self.assertFalse(response)




