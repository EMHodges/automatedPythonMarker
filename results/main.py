import importlib
import unittest

from results.utils import extractMethodNames
from static_lint.lint_answer import lint_answer
from .models import Result
from .apps import QUESTION_TEST_FILES, QUESTION_RUNNERS


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_questions(question_number)


def run_tests_for_questions(no):
    loader = unittest.TestLoader()
    suite = loader.discover('results', pattern=f'test_question_{no}.py')
    question_runner = QUESTION_RUNNERS[no]
    question_runner.run(suite)


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
