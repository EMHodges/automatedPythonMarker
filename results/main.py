import unittest

from static_lint.lint_answer import lint_answer
from .apps import QUESTION_RUNNERS
from .utils import class_registers, class_register


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_questions(question_number)


def run_tests_for_questions(no):
    loader = unittest.TestLoader()
    suite = loader.discover('configs', pattern=f'test_question_{no}.py')
    question_runner = QUESTION_RUNNERS[no]
    question_runner.run(suite)


