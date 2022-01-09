import ast
import functools

from results.QuestionsTestCase import QuestionsTestCase
from results.apps import QUESTION_TEST_FILES


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case_instance: QuestionsTestCase = args[0]
            func(*args, **kwargs)
            test_case_instance.mark = max_mark
        return decorated
    return decorator


def extractTestNames(question_number):
    source = open(QUESTION_TEST_FILES[question_number]).read()

    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == f'TestQuestion{question_number}':
            return [function.name for function in node.body if isinstance(function, ast.FunctionDef) and function.name.startswith("test")]
