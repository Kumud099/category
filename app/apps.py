from django.apps import AppConfig


class AppConfigCustom(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
