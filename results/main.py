import ast
import functools
import importlib
import unittest

import timeout_decorator

from automatedPythonMarker.settings import resource_path
from results import QuestionsTestCase
from results.resultsEnum import ResultsEnum
from static_lint.lint_answer import lint_answer
from static_lint.models import StaticLint
from .models import Result
from .apps import QUESTION_TEST_FILES

QUESTION_RUNNERS = {}
# QUESTION_TEST_FILES = {}


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    lint_errors = StaticLint.objects.get(question_number=question_number).feedback

    run_tests_for_question(question_number)


def run_tests_for_question(question_number):
    question_runner = QUESTION_RUNNERS[question_number]
    spec = importlib.util.spec_from_file_location('yo', QUESTION_TEST_FILES[question_number])
    module = importlib.util.module_from_spec(spec)
    Result.objects.all().delete()
    print(Result.objects.all())
    try:
        spec.loader.exec_module(module)

    except ImportError:
        Result.error_tests_for_question(question_number, 'Import Error')
    #    test_names = extractTestNames(question_number)
    #    for i in test_names:
    #        Result.objects.update_or_create(question_number=question_number, test_name=i,
     #                                       defaults={
      #                                          'test_result': ResultsEnum.ERROR,
       #                                         'test_feedback': '',
        #                                        'mark': 0
         #                                   })
    except SyntaxError:
        Result.error_tests_for_question(question_number, 'Syntax Error')

    suite = unittest.TestLoader().loadTestsFromModule(module)
    run_suite(question_runner, suite)


def run_suite(question_runner, suite):
    question_runner.run(suite)


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case_instance: QuestionsTestCase = args[0]
            func(*args, **kwargs)
            test_case_instance.mark = max_mark
        return decorated
    return decorator


if __name__ == "__main__":
    run_tests_for_question('yo', 'test_question_1.py')
