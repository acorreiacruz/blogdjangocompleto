from django.apps import AppConfig


class AutoresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'autores'

    def ready(self, *args, **kwargs):
        import autores.signals #noqa
        return super().ready(*args, **kwargs)
