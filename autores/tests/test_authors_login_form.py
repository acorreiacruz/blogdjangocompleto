from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from parameterized import parameterized
from autores.forms import LoginForm


class LoginFormUnitTest(TestCase):
    
    @parameterized.expand([
        ('password',''),
    ])
    def test_if_fields_label_is_correct(self, field, label):
        form = LoginForm()
        label_test = form[field].field.label
        self.assertEqual(label_test, label)
        