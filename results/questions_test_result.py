import unittest

from results.models import Result, Subtest
from results.questions_test_case import QuestionsTestCase
from results.results_enum import ResultsEnums


class QuestionsTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super(QuestionsTestResult, self).__init__(stream, descriptions, verbosity)

    # ToDo add these to the results database
    def addSubTest(self, test: QuestionsTestCase, subtest, err):
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                addSubTestResult(test, subtest, ResultsEnums.FAIL)
                errors = self.failures
            else:
                addSubTestResult(test, subtest, ResultsEnums.ERROR)
                errors = self.errors
            errors.append((subtest, self._exc_info_to_string(err, test)))
            self._mirrorOutput = True


def addSubTestResult(test: QuestionsTestCase, subtests, result: ResultsEnums):
    r = Result.objects.get_or_none(question_number=test.get_question_number(), test_name=test.methodName)
    Subtest.objects.update_or_create(identifier=subtests.id(), defaults={
        'message': subtests._message,
        'test_result': result,
        'test': r
    })
    print(Subtest.objects.all())
    print(r.subtest_set.all())
