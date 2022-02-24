import unittest

from results.models import Result, Subtest
from results.questions_test_case import QuestionsTestCase
from results.results_enum import ResultsEnums


class QuestionsTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super(QuestionsTestResult, self).__init__(stream, descriptions, verbosity)

    def addSubTest(self, test: QuestionsTestCase, subtest, err):
        print(err)
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
    r = Result.objects.get(question_number=test.get_question_number(),
                           question_part=test._get_question_part(),
                           test_name=test.methodName)
    r.update_test_result(result, feedback)
    Subtest.objects.update_or_create(identifier=subtest.id(), defaults={
        'params_failing': subtest._message,
        'part': test._get_question_part(),
        'test_result': result,
        'test': r
    })