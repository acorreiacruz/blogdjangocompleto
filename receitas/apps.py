from django.apps import AppConfig


class ReceitasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'receitas'

    def ready(self, *args, **kwargs):
        import receitas.signals # noqa
        return super().ready(*args, **kwargs)
