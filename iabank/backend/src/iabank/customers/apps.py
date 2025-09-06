from django.apps import AppConfig


class CustomersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'iabank.customers'
    verbose_name = 'IABANK Customers'
