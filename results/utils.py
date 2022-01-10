import ast
import functools
import sys

from automatedPythonMarker.settings import resource_path
from results.questions_test_case import QuestionsTestCase
from results.apps import QUESTION_TEST_FILES


def extractTestNames(question_number):
    source = open(QUESTION_TEST_FILES[question_number]).read()

    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == f'TestQuestion{question_number}':
            return [function.name for function in node.body if
                    isinstance(function, ast.FunctionDef) and function.name.startswith("test")]


def extractMethodNames():
    print('in extract')
    source = open(resource_path('static_lint/code_to_lint.py')).read()
    print(source)
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
            import importlib
            f = importlib.import_module('static_lint.code_to_lint')
            print(dir(f))
            c = extractMethodNames()
            print(c)
            g = 'calculateFine'
            test_case_instance: QuestionsTestCase = args[0]
            if c[0] != g:
                test_case_instance.fail("@Import error")
            func(*args, **kwargs)
            test_case_instance.mark = max_mark

        return decorated

    return decorator
