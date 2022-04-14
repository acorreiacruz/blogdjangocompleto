import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.[A-Z])(?=.[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'Sua senha deve conter no mínimo 8 caracteres ,sendo pelo menos um maiúsculo,\
             e deve possuir pelo menos um número',
            code='invalid',
        )


class RegisterForm(forms.ModelForm):

    first_name = forms.CharField(
        required = True,
        label = "Primeiro Nome",
        label_suffix = ":",
        max_length = 30,
        min_length = 3,
        help_text = "Insira o seu primeiro nome",
        widget = forms.TextInput(attrs={
            'placeholder': 'Ex.: antonio',
        }),
        error_messages = {
            'required': "O campo de primeiro nome não pode ficar vazio!",
            'max_length': "O primeiro nome deve ter no máximo 30 caracteres!",
            'min_length': "O primeiro nome deve ter no mínimo 3 caracteres!",
        },
    )

    last_name = forms.CharField(
        required = True,
        label = "Último Nome",
        label_suffix = ":",
        max_length = 30,
        min_length = 3,
        help_text = "Insira o seu último nome",
        widget = forms.TextInput(attrs={
            'placeholder': 'Ex.: junior',
        }),
        error_messages = {
            'required': "O campo de último nome não pode ficar vazio!",
            'max_length': "O último nome deve ter no máximo 30 caracteres!",
            'min_length': "O último nome deve ter no mínimo 3 caracteres!",
        },
    )

    username = forms.CharField(
        required = True,
        label = "Nome de Usuário",
        label_suffix = ":",
        max_length = 40,
        min_length = 3,
        help_text = "Insira o seu nome de usuário",
        widget = forms.TextInput(attrs={
            'placeholder': 'Ex.: antoniocorreia',
        }),
        error_messages = {
            'required': "O campo de nome de usuário nome não pode ficar vazio!",
            'max_length': "O nome de usuário deve ter no máximo 30 caracteres!",
            'min_length': "O nome de usuário deve ter no mínimo 3 caracteres!",
        },
    )

    email = forms.CharField(
        required = True,
        label = "E-mail",
        label_suffix = ":",
        help_text = "Insira o endereço de e-mail",
        widget = forms.EmailInput(attrs={
            'placeholder': 'Ex.: email@email.com',
        }),
        error_messages = {
            'required': "O campo de e-mail não pode ficar vazio!",
        },
    )

    password = forms.CharField(
        required = True,
        label = "Senha",
        label_suffix = ":",
        help_text = "Crie uma senha para sua conta",
        widget = forms.PasswordInput(attrs={
            'placeholder': "Insira sua senha",
        }),
        error_messages = {
            'required': "O campo de senha não pdoe ficar vazio!",
        },
        validators= [
            strong_password,
        ],
    )

    password_confirmation = forms.CharField(
        required=True,
        label = "Confirmação de Senha",
        label_suffix = ":",
        help_text = "Insira novamente a sua senha",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme a sua senha',
        }),
        error_messages = {
            'required': 'O campo de confirmação de senha não pode ficar vazio',
        }  ,
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]


    def clean_username(self):
        username_data = self.cleaned_data.get('username','')
        exist = User.objects.filter(username=username_data).exists()

        if exist:
            raise ValidationError(
                'Nome de usuário já cadastro, insira um novo!',
                code = 'invalid',
            )
        
        return username_data


    def clean_email(self):
        email_data = self.cleaned_data.get('email','')
        exist = User.objects.filter(email=email_data).exists()

        if exist:
            raise ValidationError(
                "Endereço de e-mail já cadastrado, insira um válido!",
                code = "invalid",
            )
        
        return email_data


    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise ValidationError({
                'password': ValidationError(
                    'Ambas a senhas devem ser iguais!',
                    code='invalid',
                ),
                'password_confirmation': ValidationError(
                    'Ambas a senhas devem ser iguais!',
                    code='invalid',
                ),
            })


class LoginForm(forms.Form):

    username= forms.CharField(
        required = True,
        label = "Nome de Usuário",
        label_suffix = ':',
        min_length = 3,
        max_length = 20,
        help_text = "Digite a senha da sua conta!",
        widget = forms.TextInput(attrs={
            'placeholder': 'Ex.: antoniocorreia',
        }),
        error_messages = {
            'required': "O campo de nome de usuário não pode ficar vazio!",
            'max_length': "O nome de usuário deve ter no máximo 20 caracteres, ensira um com tamanho válido!",
            'min_length': 'O nome de usuário deve ter no mínimo 3 caracteres, encira um com tamango válido!',
        },
    )

    password = forms.CharField(
        required = True,
        label = "Senha",
        label_suffix = ":",
        help_text = "Insira a sua senha de usuário já cadastrada",
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Insira sua senha de usuário',
        }),
        error_messages= {
            'required': "O campo de senha não pode ficar vazio!",
        }
    )
