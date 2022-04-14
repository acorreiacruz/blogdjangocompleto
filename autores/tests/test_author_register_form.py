from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from autores.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class RegisterFormUnitTest(TestCase):


    @parameterized.expand([
        ('first_name','Primeiro Nome'),
        ('last_name','Último Nome'),
        ('username','Nome de Usuário'),
        ('email','E-mail'),
        ('password','Senha'),
        ('password_confirmation','Confirmação de Senha'),
    ])
    def test_if_fields_label_is_correct(self, field, label):
        form = RegisterForm()
        label_test = form[field].field.label
        self.assertEqual(label, label_test)


    @parameterized.expand([
        ('first_name','Insira o seu primeiro nome'),
        ('last_name','Insira o seu último nome'),
        ('username','Insira o seu nome de usuário'),
        ('email','Insira o endereço de e-mail'),
        ('password','Crie uma senha para sua conta'),
        ('password_confirmation','Insira novamente a sua senha'),
    ])
    def test_if_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        help_text_test = form[field].field.help_text
        self.assertEqual(help_text_test, help_text)
    

    @parameterized.expand([
        ('first_name','Ex.: antonio'),
        ('last_name','Ex.: junior'),
        ('username','Ex.: antoniocorreia'),
        ('email','Ex.: email@email.com'),
        ('password','Insira sua senha'),
        ('password_confirmation','Confirme a sua senha'),
    ])
    def test_if_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        placeholder_test = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, placeholder_test)

    
    @parameterized.expand([
        ('first_name','O campo de primeiro nome não pode ficar vazio!'),
        ('last_name','O campo de último nome não pode ficar vazio!'),
        ('username','O campo de nome de usuário nome não pode ficar vazio!'),
        ('email','O campo de e-mail não pode ficar vazio!'),
        ('password','O campo de senha não pdoe ficar vazio!'),
        ('password_confirmation','O campo de confirmação de senha não pode ficar vazio'),
    ])
    def test_if_fields_error_messages_required_is_correct(self, field, required):
        form = RegisterForm()
        required_test = form[field].field.error_messages['required']
        self.assertEqual(required_test, required)


class RegisterFormIntegrationTest(DjangoTestCase):

    def setUp(self) -> None:
        self.form_data = {
            'first_name': 'Jhon',
            'last_name': 'Doe',
            'username': 'jhondoe',
            'email': 'jhondoe@email.com',
            'password': 'P@as1234',
            'password_confirmation': 'P@as1234',
        }
        return super().setUp()


    @parameterized.expand([
        ('first_name','O campo de primeiro nome não pode ficar vazio!'),
        ('last_name','O campo de último nome não pode ficar vazio!'),
        ('username','O campo de nome de usuário nome não pode ficar vazio!'),
        ('email','O campo de e-mail não pode ficar vazio!'),
        ('password','O campo de senha não pdoe ficar vazio!'),
        ('password_confirmation','O campo de confirmação de senha não pode ficar vazio'),
    ])
    def test_if_fields_required_message_is_being_render(self, field, msg):
        url = reverse('autores:register_validate')
        self.form_data[field] = ''
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field,''))

    
    @parameterized.expand([
        ('first_name','O campo de primeiro nome não pode ficar vazio!'),
        ('last_name','O campo de último nome não pode ficar vazio!'),
        ('username','O campo de nome de usuário nome não pode ficar vazio!'),
        ('email','O campo de e-mail não pode ficar vazio!'),
        ('password','O campo de senha não pdoe ficar vazio!'),
        ('password_confirmation','O campo de confirmação de senha não pode ficar vazio'),
    ])
    def test_if_fields_required_message_is_not_being_render(self, field, msg):
        url = reverse('autores:register_validate')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get(field, ''))


    def test_if_register_view_raise_404_on_get_method(self):
        url = reverse('autores:register_validate')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
    def test_if_email_field_dont_raise_invalid_error_message_if_unique(self):
        url = reverse('autores:register_validate')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Endereço de e-mail já cadastrado, insira um válido!'
        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('email', ''))


    def test_if_email_field_raise_invalid_error_message_if_not_unique(self):
        url = reverse('autores:register_validate')
        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Endereço de e-mail já cadastrado, insira um válido!'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('email', ''))


    def test_if_username_field_dont_raise_invalid_error_message_if_unique(self):
        url = reverse('autores:register_validate')
        response = self.client.post(url , data=self.form_data, follow=True)
        msg = 'Nome de usuário já cadastro, insira um novo!'
        self.assertNotIn(msg, response.content.decode('utf-8'))
        self.assertNotIn(msg, response.context['form'].errors.get('username', ''))
    
    def test_if_username_field_raise_invalid_error_message_if_not_unique(self):
        url = reverse('autores:register_validate')
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url , data=self.form_data, follow=True)
        msg = 'Nome de usuário já cadastro, insira um novo!'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username', ''))



