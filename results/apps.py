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
        from questions.models import QuestionComposite

        questions = QuestionComposite.objects.all()
        for question in questions:
            sub_questions = question.subquestioncomposite_set.all()
            for sub_question in sub_questions:
                keys = []
                for key, value in QUESTION_RUNNERS.items():
                    keys.append(key)
                if question.number in keys:
                    exists = QUESTION_RUNNERS[question.number]
                    exists[sub_question.part] = QuestionsTestRunner(question.number, sub_question.part)
                else:
                    QUESTION_RUNNERS[question.number] = {sub_question.part: QuestionsTestRunner(question.number, sub_question.part)}
            self._add_test_file_paths(question.number)
        self._extract_model_functions(1)

    def _add_test_file_paths(self, question_number):
        from automatedPythonMarker.settings import resource_path

        test_files = [test_file for test_file in listdir(resource_path("configs")) if
                      isfile(join(resource_path("configs"), test_file)) and test_file.startswith('test_question_')]

        for test_file in test_files:
            if test_file.startswith(f'test_question_{str(question_number)}'):
                question_part = self._extract_question_part_from_file_name(test_file, question_number)
                keys = []
                test_file = os.path.join("configs", test_file)
                for key, value in QUESTION_TEST_FILES.items():
                    keys.append(key)

                if question_number in keys:
                    exists = QUESTION_TEST_FILES[question_number]
                    exists[question_part] = test_file
                else:
                    QUESTION_TEST_FILES[question_number] = {question_part: test_file}

    @staticmethod
    def _extract_question_part_from_file_name(test_file_name, question_number) -> int:
        question_part = test_file_name.replace(f'test_question_{str(question_number)}', '')\
                                      .replace('.py', '')
        return roman.fromRoman(question_part.upper())

    @staticmethod
    def _extract_model_functions(question_number):
        source = open(resource_path(os.path.join('configs', f'model_answer_question_{question_number}.py'))).read()
        functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
        for function in functions:
            docstring = ast.get_docstring(function)
            question_part = int(re.findall(r'\d+', docstring)[0])
            keys = []
            for key, value in MODEL_ANSWERS.items():
                keys.append(key)
            if question_number in keys:
                exists = MODEL_ANSWERS[question_number]
                keyss = []
                for key, value in exists.items():
                    keyss.append(key)
                if question_part in keyss:
                    exists[question_part].append(ast.get_source_segment(source, function))
                else:
                    exists[question_part] = [ast.get_source_segment(source, function)]
            else:
                functions = {question_part: [ast.get_source_segment(source, function)]}
                MODEL_ANSWERS[question_number] = functions


