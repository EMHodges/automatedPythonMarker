import os
import shutil
import unittest

import roman

from automatedPythonMarker.settings import resource_path
from questions.models import QuestionComposite, SubQuestionComposite
from results.apps import QUESTION_RUNNERS, MODEL_ANSWERS
from static_lint.lint_answer import lint_answer
from submission.models import Submission

TMP_FILE = resource_path(os.path.join('static_lint', 'code_to_lint.py'))


def run_tests(answer, question_number, question_part, submission):
    construct_test_file(answer, question_number, question_part)
    lint_answer(question_number, submission, question_part)
    run_tests_for_question_part(question_number, question_part)


def create_submission(question_number, question_part):
    question = QuestionComposite.objects.get(number=question_number)
    sub_question = SubQuestionComposite.object.get(question=question, part=question_part)
    submission_number = Submission.object.get_next_submission_number(sub_question)
    submission = Submission.object.create(sub_question=sub_question, submission_number=submission_number)
    submission.save()
    return Submission.object.get_last_submission(sub_question)


def construct_test_file(answer, question_number, question_part_submitted):
    model_answers = MODEL_ANSWERS.get(question_number)
    shutil.rmtree(TMP_FILE, ignore_errors=True)
    with open(TMP_FILE, 'w') as tmp_file:
        for question_part, model_answer_functions in model_answers.items():
            if question_part == question_part_submitted:
                tmp_file.write(answer + '\n \n')
                break
            else:
                for model_answer_function in model_answer_functions:
                    tmp_file.write(model_answer_function + '\n \n')


def run_tests_for_question_part(question_number, question_part):
    loader = unittest.TestLoader()
    question_part_roman = roman.toRoman(question_part).lower()
    suite = loader.discover('configs', pattern=f'test_question_{question_number}{question_part_roman}.py')
    question_runner = QUESTION_RUNNERS[question_number][question_part]
    question_runner.run(suite)
