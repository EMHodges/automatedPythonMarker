import unittest

from results.QuestionsTestCase import QuestionsTestCase
from results.models import Result
from results.resultsEnum import ResultsEnum


class QuestionsTextTestResult(unittest.TextTestResult):
    '''
    classdocs
    '''
    def __init__(self, question_number, stream='yo.txt', descriptions=True, verbosity=None):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure
         compatibility as the
        interface changes.
        """
        self.question_number = question_number
        super(QuestionsTextTestResult, self).__init__(stream, descriptions, verbosity)

    def addSuccess(self, test: QuestionsTestCase) -> None:
        unittest.TestResult.addSuccess(self, test)
        self.create_result(test, ResultsEnum.SUCCESS, "Success")

    def addError(self, test: QuestionsTestCase, err) -> None:
        self.create_result(test, ResultsEnum.ERROR, "ERROR!\\newline " + format_err(str(err[1])))

    def addFailure(self, test: QuestionsTestCase, err) -> None:
        unittest.TestResult.addFailure(self, test, err)
        self.create_result(test, ResultsEnum.FAIL, "Failed!\\newline " + format_err(str(err[1])))

    def create_result(self, test: QuestionsTestCase, test_result: ResultsEnum, test_feedback: str) -> None:
        Result.objects.update_or_creates(self.question_number, test.methodName, test_result, test_feedback, test.mark)


def format_err(err) -> str:
    message_index = err.rfind('@')
    if message_index < 0 or message_index >= len(err) - 1:
        return ""
    else:
        return err[message_index + 1:]
