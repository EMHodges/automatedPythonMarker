import ast
import functools
import importlib

from automatedPythonMarker.settings import resource_path
from questions.models import Question
from results.questions_test_case import QuestionsTestCase
from results.apps import QUESTION_TEST_FILES
from static_lint.models import StaticLint
import re


class RegisterTestClass:
    test_method_names_for_question = {}

    def __init__(self, question_number, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._question_number = question_number

    def __call__(self, cls):
        test_methods = [method for method in dir(cls) if method.startswith('test')]
        self.test_method_names_for_question[self._question_number] = test_methods
        return cls


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case_instance: QuestionsTestCase = args[0]

            check_import_error(test_case_instance)
            func(*args, **kwargs)
            test_case_instance.set_mark(max_mark)

        return decorated

    return decorator


def extract_method_names():
    source = open(resource_path('static_lint/code_to_lint.py')).read()
    return [node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]


def check_import_error(test_case: QuestionsTestCase) -> None:
    module_method_names = extract_method_names()
    question_number = test_case.get_question_number()
    method_under_test = Question.objects.get(number=question_number).method_name
    if method_under_test not in module_method_names:
        test_case.fail("@Import error")


def check_syntax_error(test_case: QuestionsTestCase) -> None:
    test_case_class_name = test_case.__class__.__name__
    test_case_question_number = re.split('TestQuestion', test_case_class_name)[-1]

    syntax_errors_for_question = StaticLint.objects.get(question_number=int(test_case_question_number))

    if syntax_errors_for_question.feedback:
        test_case.fail("@Syntax error")


def extract_test_names(question_number):
    source = open(QUESTION_TEST_FILES[question_number]).read()

    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == f'TestQuestion{question_number}':
            return [function.name for function in node.body if
                    isinstance(function, ast.FunctionDef) and function.name.startswith("test")]
