import unittest

from results.questions_test_case import QuestionsTestCase
from results.models import Result
from results.questions_test_result import QuestionsTestResult
from results.results_enum import ResultsEnums


class QuestionsTextTestResult(QuestionsTestResult):
    '''
    classdocs
    '''

    def __init__(self, question_number, question_part, stream=None, descriptions=True, verbosity=1):
        """Construct a TextTestRunner.

        Subclasses should accept **kwargs to ensure
         compatibility as the
        interface changes.
        """
        if not isinstance(question_number, int):
            raise TypeError("question_number must be an integer")

        self.question_number = question_number
        self.question_part = question_part
        super(QuestionsTextTestResult, self).__init__(stream, descriptions, verbosity)

    def addSuccess(self, test: QuestionsTestCase) -> None:
        unittest.TestResult.addSuccess(self, test)
        self.create_result(test, ResultsEnums.SUCCESS, "Success")

    def addError(self, test: QuestionsTestCase, err) -> None:
        err_name = err[0].__name__
        print('poop')
        print(err[0])
        print(err[1])
        if err_name == 'SyntaxError':
            self._addSyntaxError(test)
        else:
            self.create_result(test, ResultsEnums.ERROR, f"ERROR! {format_err(str(err[1]))}")

    def addFailure(self, test: QuestionsTestCase, err) -> None:
        unittest.TestResult.addFailure(self, test, err)
        self.create_result(test, ResultsEnums.FAIL, f"Failed! {format_err(str(err[1]))}")

    def create_result(self, test: QuestionsTestCase, test_result, test_feedback: str) -> None:
        Result.objects.update_or_create(question_number=self.question_number,
                                        question_part=self.question_part,
                                        test_name=test.methodName,
                                        defaults={
                                            'test_feedback': test_feedback,
                                            'test_result': test_result,
                                            'mark': test.get_mark()
                                        })

    def _addSyntaxError(self, test: QuestionsTestCase):
        self.create_result(test, "ERROR! Syntax Error")


def format_err(err) -> str:
    message_index = err.rfind('@')
    if message_index < 0 or message_index >= len(err) - 1:
        return ""
    else:
        return err[message_index + 1:]
