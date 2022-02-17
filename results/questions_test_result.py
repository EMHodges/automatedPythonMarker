import unittest

from results.models import Result, Subtest
from results.questions_test_case import QuestionsTestCase
from results.results_enum import ResultsEnums


class QuestionsTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super(QuestionsTestResult, self).__init__(stream, descriptions, verbosity)

    def addSubTest(self, test: QuestionsTestCase, subtest, err):
        if err is None:
            addSubTestResult(test, subtest, ResultsEnums.SUCCESS)
        else:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                addSubTestResult(test, subtest, ResultsEnums.FAIL)
            else:
                addSubTestResult(test, subtest, ResultsEnums.ERROR)


def addSubTestResult(test: QuestionsTestCase, subtest, result: ResultsEnums):
    r = Result.objects.get(question_number=test.get_question_number(), test_name=test.methodName)
    Subtest.objects.update_or_create(identifier=subtest.id(), defaults={
        'params_failing': subtest._message,
        'test_result': result,
        'test': r
    })