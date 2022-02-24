import ast
import os.path
import re
from os import listdir
from os.path import isfile, join

import roman

from django.apps import AppConfig

from automatedPythonMarker.settings import resource_path

QUESTION_TEST_FILES = {}
QUESTION_RUNNERS = {}
MODEL_ANSWERS = {}


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'

    def ready(self):
        self._setup_testRunner_for_questions()

    def _setup_testRunner_for_questions(self):
        from .question_test_runner import QuestionsTestRunner
        from questions.models import Question

        number_of_questions = Question.objects.values_list('number', flat=True)
        for question_number in number_of_questions:
            QUESTION_RUNNERS[question_number] = QuestionsTestRunner(question_number)
            self._add_test_file_paths(question_number)
        self._extract_model_functions(4)

    def _add_test_file_paths(self, question_number):
        from automatedPythonMarker.settings import resource_path

        onlyfiles = [f for f in listdir("configs") if isfile(join("configs", f)) and f.startswith('t_test')]

        for i in onlyfiles:
            if i.startswith(f't_test_question_{str(question_number)}'):
                j = i.removeprefix(f't_test_question_{str(question_number)}').removesuffix('.py').upper()
                j = roman.fromRoman(j)
                keys = []
                i = os.path.join("configs", i)
                for key, value in QUESTION_TEST_FILES.items():
                    keys.append(key)

                if question_number in keys:
                    exists = QUESTION_TEST_FILES[question_number]
                    exists[j] = i
                else:
                    QUESTION_TEST_FILES[question_number] = {j: i}

    def _extract_model_functions(self, question_number):
        source = open(resource_path('configs/t_model_answer_question_4.py')).read()
        x = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
        for i in x:
            docstring = ast.get_docstring(i)
            c = int(re.findall(r'\d+', docstring)[0])
            keys = []
            for key, value in MODEL_ANSWERS.items():
                keys.append(key)
            if question_number in keys:
                exists = MODEL_ANSWERS[question_number]
                keyss = []
                for key, value in exists.items():
                    keyss.append(key)
                if c in keyss:
                    exists[c].append(ast.get_source_segment(source, i))
                else:
                    exists[c] = [ast.get_source_segment(source, i)]
            else:
                x = {c: [ast.get_source_segment(source, i)]}
                MODEL_ANSWERS[question_number] = x
        print(MODEL_ANSWERS)


