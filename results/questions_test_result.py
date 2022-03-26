import unittest

from questions.models import QuestionComposite, SubQuestionComposite
from results.models import Result, Subtest
from results.questions_test_case import QuestionsTestCase
from results.results_enum import ResultsEnums
from submission.models import Submission


class QuestionsTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super(QuestionsTestResult, self).__init__(stream, descriptions, verbosity)

    def addSubTest(self, test: QuestionsTestCase, subtest, err):
        if err is None:
            addSubTestResult(test, subtest, 'Success', ResultsEnums.SUCCESS)
        else:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                addSubTestResult(test, subtest, 'Failed', ResultsEnums.FAIL)
            else:
                addSubTestResult(test, subtest, 'Error', ResultsEnums.ERROR)


def addSubTestResult(test: QuestionsTestCase, subtest, feedback, result: ResultsEnums):
    question = QuestionComposite.objects.get(number=test.get_question_number())
    sub_question = SubQuestionComposite.object.get(question=question, part=test._get_question_part())
    submission_number = Submission.object.get_last_submission_number(sub_question)
    submission = Submission.object.get(sub_question=sub_question, submission_number=submission_number)

    r = Result.objects.get(question_number=test.get_question_number(),
                           question_part=test._get_question_part(),
                           submission=submission,
                           test_name=test.methodName)
    r.update_test_result(result, feedback)
    message = subtest._message
    if isinstance(subtest._message, tuple):
        args = list(subtest._message)
        message = tuple(args[1:])
    Subtest.objects.update_or_create(identifier=subtest.id(), defaults={
        'params_failing': message,
        'part': test._get_question_part(),
        'test_result': result,
        'test': r
    })