from django.apps import AppConfig


class DeThiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.de_thi'

    def ready(self):
        """Import signals when app is ready"""
        import apps.de_thi.signals
