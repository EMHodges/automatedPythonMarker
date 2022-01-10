import functools
import importlib
import sys
import unittest


from results.questions_test_case import QuestionsTestCase
from results.utils import extractMethodNames
from static_lint.lint_answer import lint_answer
from .models import Result
from .apps import QUESTION_TEST_FILES

from unittest import main
from .test_question_1 import TestQuestion1

# Todo move this into apps
QUESTION_RUNNERS = {}


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_questions(question_number)

def run_lub():
    extractMethodNames()

def run_tests_for_questions(no):
    import unittest
    loader = unittest.TestLoader()
    start_dir = 'results/test_question_1.py'
    suite = loader.discover('results', pattern='test_question_1.py')

    runner = unittest.TextTestRunner()
    x = QUESTION_RUNNERS[no]
    try:
        b = x.run(suite)
    except Exception as e:
        print('in exception')
        print(e)
    print('b')
    print(b)



# Todo debug in EXE it won't go into the Import or Syntax Error
def run_tests_for_question(question_number):
    importlib.invalidate_caches()
    question_runner = QUESTION_RUNNERS[question_number]
    spec = importlib.util.spec_from_file_location('yo', QUESTION_TEST_FILES[question_number])
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)
        suite = unittest.TestLoader().loadTestsFromModule(module)
        run_suite(question_runner, suite)

    except ImportError:
        Result.objects.error_tests_for_question(question_number, 'Import Error')

    except SyntaxError:
        Result.objects.error_tests_for_question(question_number, 'Syntax Error')


def run_suite(question_runner, suite):
    question_runner.run(suite)




if __name__ == "__main__":
    run_tests_for_question('yo', 'test_question_1.py')
