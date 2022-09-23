import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from receitas.models import Receitas
from collections import defaultdict
from utils.validators import is_positive_number


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.[A-Z])(?=.[0-9]).{8,}$')
    if not regex.match(password):
        raise ValidationError(
            'Sua senha deve conter no mínimo 8 caracteres ,sendo pelo menos um maiúsculo, e deve possuir pelo menos um número',
            code='invalid'
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
            'required': "O campo de senha não pode ficar vazio!",
        },
        # validators= [
        #     strong_password,
        # ],
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

        return cleaned_data


class LoginForm(forms.Form):

    username= forms.CharField(
        required = True,
        label = "Nome de Usuário",
        label_suffix = ':',
        min_length = 3,
        max_length = 20,
        help_text = "Digite o seu nome de usuário",
        widget = forms.TextInput(attrs={
            'placeholder': 'Ex.: antoniocorreia',
        }),
        error_messages = {
            'required': "O campo de nome de usuário não pode ficar vazio!",
            'max_length': "O nome de usuário deve ter no máximo 20 caracteres, ensira um com tamanho válido!",
            'min_length': 'O nome de usuário deve ter no mínimo 3 caracteres, ensira um com tamango válido!',
        },
    )

    password = forms.CharField(
        required = True,
        label = "Senha",
        label_suffix = ":",
        help_text = "Insira a sua senha já cadastrada",
        widget = forms.PasswordInput(attrs={
            'placeholder': 'Insira sua senha',
        }),
        error_messages= {
            'required': "O campo de senha não pode ficar vazio!",
        }
    )


class EditRecipeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_errors = defaultdict(list)

    class Meta:
        model=Receitas
        fields= [
            'title', 'description',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit', 'preparation_step',
            'description','cover',
        ]

        widgets = {
            'preparation_step': forms.Textarea(
                attrs={
                    'class': 'span-2'
                }
            ),
            'cover': forms.FileInput(
                attrs={
                    'class': 'span-2'
                }
            ),
            'servings_unit': forms.Select(
                choices=(
                    ('Pessoas','Pessoas'),
                    ('Pedaços','Pedaços'),
                    ('Porções','Porções')
                )
            ),
            'preparation_time_unit': forms.Select(
                choices=(
                    ('Minutos','Minutos'),
                    ('Horas','Horas')
                )
            ),
        }

    def clean_preparation_time(self):
        preparation_time = self.cleaned_data.get('preparation_time')

        if not is_positive_number(preparation_time):
            self.form_errors['preparation_time'].append(
                'O tempo de preparo deve ser um número positivo'
            )

        return preparation_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')

        if not is_positive_number(servings):
            self.form_errors['servings'].append(
                'A porção deve ser um número positivo'
            )

        return servings

    def clean(self,*args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        preparation_step = self.cleaned_data.get('preparation_step')

        if len(title) < 10:
            self.form_errors['title'].append(
                'O título deve conter pelo menos 10 caracteres'
            )

        if len(description) < 20:
            self.form_errors['description'].append(
                'A descrição deve conter pelo menos 20 caracteres'
            )

        if len(preparation_step) < 100:
            self.form_errors['preparation_step'].append(
                'Os passos de preparo deve conter pelo menos 100 caracteres'
            )

        if description == title:
            self.form_errors['description'].append(
                'A descrição não pode ser igual ao título'
            )
            self.form_errors['title'].append(
                'O título não pode ser igual a descrição'
            )

        if self.form_errors:
            raise ValidationError(self.form_errors)

        return super_clean


