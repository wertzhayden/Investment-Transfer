from django.apps import AppConfig


class FinancingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "financing"

    def ready(self):
        import financing.signals  # noqa
