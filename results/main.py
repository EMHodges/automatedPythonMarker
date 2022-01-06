import importlib
import unittest
from automatedPythonMarker.settings import resource_path
from static_lint.lint_answer import lint_answer
from static_lint.models import StaticLint

QUESTION_RUNNERS = {}
QUESTION_TEST_FILES = {}


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    lint_errors = StaticLint.objects.get(question_number=question_number).feedback
    if not lint_errors:
        run_tests_for_question(question_number)


def run_tests_for_question(question_number):
    question_runner = QUESTION_RUNNERS[question_number]
    spec = importlib.util.spec_from_file_location('yo', QUESTION_TEST_FILES[question_number])
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError:
        suite = unittest.TestLoader().loadTestsFromModule(module)
        print('not implemented')
    suite = unittest.TestLoader().loadTestsFromModule(module)
    run_suite(question_runner, suite)


def run_suite(question_runner, suite):
    question_runner.run(suite)


if __name__ == "__main__":
    run_tests_for_question('yo', 'test_question_1.py')
