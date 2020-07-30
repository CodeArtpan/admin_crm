from django.apps import AppConfig


class CrmConfig(AppConfig):
    name = 'crm'

    def ready(self):
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('entrance')
