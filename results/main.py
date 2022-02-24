import os
import shutil
import unittest

from automatedPythonMarker.settings import resource_path
from results.apps import QUESTION_RUNNERS, MODEL_ANSWERS
from results.models import Result
from results.utils import extract_model_functions
from static_lint.lint_answer import lint_answer, linting_answer

TMP_FILE = resource_path(os.path.join('static_lint', 'code_to_lint.py'))


def run_tests(answer, question_number):
    lint_answer(answer, question_number)
    run_tests_for_question(question_number)


def run_testing(answer, question_number, question_part):
    construct_test_file(answer, question_number, question_part)
    linting_answer(question_number)
 #   extract_model_functions()


def construct_test_file(answer, question_number, question_part):
    model_answers = MODEL_ANSWERS.get(question_number)

    shutil.rmtree(TMP_FILE, ignore_errors=True)
    with open(TMP_FILE, 'w') as tmp_file:
        for key, value in model_answers.items():
            if key == question_part:
                tmp_file.write(answer + '\n \n')
            else:
                for i in value:
                    tmp_file.write(i + '\n \n')


def write_answer_to_tmp_file(answer):
    shutil.rmtree(TMP_FILE, ignore_errors=True)
    with open(TMP_FILE, 'w') as tmp_file:
        tmp_file.write(answer)



def run_tests_for_question(question_number):
    Result.objects.filter(question_number=question_number).delete()
    loader = unittest.TestLoader()
    suite = loader.discover('configs', pattern=f'test_question_{question_number}.py')
    question_runner = QUESTION_RUNNERS[question_number]
    question_runner.run(suite)
