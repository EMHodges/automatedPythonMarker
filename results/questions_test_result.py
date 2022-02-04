import unittest

from results.questions_test_case import QuestionsTestCase


class QuestionsTestResult(unittest.TestResult):

    def __init__(self, stream=None, descriptions=True, verbosity=1):
        super(QuestionsTestResult, self).__init__(stream, descriptions, verbosity)

    # ToDo add these to the results database
    def addSubTest(self, test: QuestionsTestCase, subtest, err):
        print('adding sub test dail')
        print('typezzzzzz')
        print(type(test))
        print(test.get_question_number())
        print(test.methodName)
        print(type(subtest))
        print(subtest)
        print(subtest._subDescription())
        print(subtest.id())
        print('message')
        print(subtest._message)
        print(subtest.params)
        print('finish dail')
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            if issubclass(err[0], test.failureException):
                self.addFailure(test, err)
                errors = self.failures
            else:
                errors = self.errors
            errors.append((subtest, self._exc_info_to_string(err, test)))
            self._mirrorOutput = True

