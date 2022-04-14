from django.core.exceptions import ValidationError
from .test_receita_base import ReceitasTestBase

class ReceitaModelTest(ReceitasTestBase):

    def setUp(self) -> None:
        self.receita = self.make_receita()
        return super().setUp()

    def test_receita_title_raises_error_if_title_has_more_than_70_chars(self):
        self.receita.title = 'A' * 10
        self.receita.save()
        
        with self.assertRaises(ValidationError):
            self.receita.full_clean()
        