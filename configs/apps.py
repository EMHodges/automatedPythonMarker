import importlib

from django.apps import AppConfig


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configs'

    def ready(self):
        print('readying')
        importlib.import_module('configs.test_question_1', 'TestQuestion1')
        importlib.import_module('configs.test_question_2', 'TestQuestion2')
        importlib.import_module('configs.t_test_question_4i', 'TestQuestion4i')
        importlib.import_module('configs.t_test_question_4ii', 'TestQuestion4ii')

    #  from .test_question_1 import TestQuestion1
    # from .test_question_2 import TestQuestion2
