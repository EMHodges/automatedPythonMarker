import os.path
import importlib

from django.apps import AppConfig

class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configs'

    def ready(self):
        import configs
        x = importlib.import_module('configs.test_question_1', 'TestQuestion1')
        x = importlib.import_module('configs.test_question_2', 'TestQuestion2')

      #  from .test_question_1 import TestQuestion1
       # from .test_question_2 import TestQuestion2
