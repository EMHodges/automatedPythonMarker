import importlib
import unittest
from automatedPythonMarker.settings import resource_path
from static_lint.lint_answer import lint_answer
from static_lint.models import StaticLint

QUESTION_RUNNERS = {}


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    lint_errors = StaticLint.objects.get(question_number=question_number).feedback
    if not lint_errors:
        run_tests_for_file('')


def run_tests_for_file(module_name, file_name='results/test_question_1.py'):
    question_runner = QUESTION_RUNNERS[1]
    spec = importlib.util.spec_from_file_location('yo', resource_path('results/test_question_1.py'))
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
    run_tests_for_file('yo', 'test_question_1.py')
