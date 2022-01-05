import unittest

from results.QuestionsTestCase import QuestionsTestCase
from results.models import Result
from results.resultsEnum import ResultsEnum


class QuestionsTextTestResult(unittest.TextTestResult):
    '''
    classdocs
    '''
    current_test = 0
    allTests = {}

    def __init__(self, question_number, stream='yo.txt', descriptions=True, verbosity=None):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure
         compatibility as the
        interface changes.
        """
        self.question_number = question_number
        self.allTest = {}
        super(QuestionsTextTestResult, self).__init__(stream, descriptions, verbosity)

    def addSuccess(self, test: QuestionsTestCase):
        self.allTest[test.testMethodName] = "Success" + str(test.mark)
        unittest.TestResult.addSuccess(self, test)
        self.create_result(test, ResultsEnum.SUCCESS, "Success")

    def addError(self, test: QuestionsTestCase, err):
        self.allTest[test.testMethodName] = "Error" + str(err)

    def addFailure(self, test: QuestionsTestCase, err):
        unittest.TestResult.addFailure(self, test, err)
        self.create_result(test, ResultsEnum.FAIL, "Failed!\\newline " + format_err(str(err[1])))

    def create_result(self, test: QuestionsTestCase, test_result, test_feedback) -> Result:
        rest = Result(
            question_number=self.question_number,
            test_name=test.testMethodName,
            test_result=test_result,
            test_feedback=test_feedback,
            mark=test.mark
        )
        rest.save()


def format_err(err):
    message_index = err.rfind('@')
    if message_index < 0 or message_index >= len(err) - 1:
        return ""
    else:
        print(err[message_index + 1:])
        return err[message_index + 1:]
