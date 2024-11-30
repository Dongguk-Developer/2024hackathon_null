from django.apps import AppConfig


class NullConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'null'
