import importlib

from django.apps import AppConfig


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configs'

    def ready(self):
        importlib.import_module('configs.test_question_1i', 'TestQuestion1i')
        importlib.import_module('configs.test_question_1ii', 'TestQuestion1ii')
        importlib.import_module('configs.test_question_1iii', 'TestQuestion1iii')
