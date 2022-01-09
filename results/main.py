import functools
import importlib
import unittest


from results import QuestionsTestCase
from static_lint.lint_answer import lint_answer

from .models import Result
from .apps import QUESTION_TEST_FILES

# Todo move this into apps
QUESTION_RUNNERS = {}


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_question(question_number)


# Todo debug in EXE it won't go into the Import or Syntax Error
def run_tests_for_question(question_number):
    question_runner = QUESTION_RUNNERS[question_number]
    spec = importlib.util.spec_from_file_location('yo', QUESTION_TEST_FILES[question_number])
    module = importlib.util.module_from_spec(spec)

    try:
        spec.loader.exec_module(module)

    except ImportError:
        Result.objects.error_tests_for_question(question_number, 'Import Error')

    except SyntaxError:
        Result.objects.error_tests_for_question(question_number, 'Syntax Error')

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
