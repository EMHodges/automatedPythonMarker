import ast
import functools
import sys

from automatedPythonMarker.settings import resource_path
from results.questions_test_case import QuestionsTestCase
from results.apps import QUESTION_TEST_FILES
import importlib

def extractTestNames(question_number):
    source = open(QUESTION_TEST_FILES[question_number]).read()

    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == f'TestQuestion{question_number}':
            return [function.name for function in node.body if
                    isinstance(function, ast.FunctionDef) and function.name.startswith("test")]


def extractMethodNames():
    source = open(resource_path('static_lint/code_to_lint.py')).read()
    f = []
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef):
            print(node.name)
            f.append(node.name)
    return f


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case_instance: QuestionsTestCase = args[0]

            module_method_names = extractMethodNames()

            method_name = 'calculateFine' # Todo make this come from the questions file
            if method_name not in module_method_names:
                test_case_instance.fail("@Import error")

            func(*args, **kwargs)
            test_case_instance.mark = max_mark

        return decorated

    return decorator
