import _thread
import ast
import functools
import os
import threading
from contextlib import contextmanager

import timeout_decorator

from automatedPythonMarker.settings import resource_path
from questions.models import QuestionComposite, SubQuestionComposite
from results.models import Result
from results.questions_test_case import QuestionsTestCase
from submission.models import Submission


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case: QuestionsTestCase = args[0]
            question = QuestionComposite.objects.get(number=test_case.get_question_number())
            sub_question = SubQuestionComposite.object.get(question=question, part=test_case._get_question_part())
            submission_number = Submission.objects.get_last_submission_number(sub_question)
            submission = Submission.objects.get(sub_question=sub_question, submission_number=submission_number)
            Result.objects.reset_mark(question_number=test_case.get_question_number(),
                                      question_part=test_case._get_question_part(),
                                      submission=submission,
                                      test_name=test_case.methodName)
            check_import_error(test_case)
            func(*args, **kwargs)
            test_case.set_mark(max_mark)

        return decorated

    return decorator


def extract_method_names():
    source = open(resource_path(os.path.join('static_lint','code_to_lint.py'))).read()
    return [node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]


def check_import_error(test_case: QuestionsTestCase):
    module_method_names = extract_method_names()
    question_number = test_case.get_question_number()
    method_under_test = QuestionComposite.objects.get(number=question_number).subquestioncomposite_set.get(part=test_case._get_question_part()).method_name
    if method_under_test not in module_method_names:
        test_case.fail(f"@Import error - ensure method is called {method_under_test} "
                       f"and has the expected number of arguments")
