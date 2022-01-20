import unittest
from .questions_text_test_result import QuestionsTextTestResult


class QuestionsTestRunner(unittest.TextTestRunner):
    '''
    classdocs
    '''
    def __init__(self, question_number):
        self.question_number = question_number
        super(QuestionsTestRunner, self).__init__()

    def _makeResult(self):
        return QuestionsTextTestResult(self.question_number, self.stream, self.descriptions, self.verbosity)
