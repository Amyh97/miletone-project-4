from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    name = 'checkout'

    def ready(self):
        # imported but not used, in __init__.py
        import checkout.signals
