from django.apps import AppConfig


class NguoiDungConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.nguoi_dung'

    def ready(self):
        import apps.nguoi_dung.signals
