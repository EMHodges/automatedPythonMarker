import unittest

from static_lint.lint_answer import lint_answer
from .apps import QUESTION_RUNNERS


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_question(question_number)


def run_tests_for_question(question_number):
    loader = unittest.TestLoader()
    suite = loader.discover('configs', pattern=f'test_question_{question_number}.py')
    question_runner = QUESTION_RUNNERS[question_number]
    question_runner.run(suite)
