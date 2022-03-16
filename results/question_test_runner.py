import unittest
from .questions_text_test_result import QuestionsTextTestResult


class QuestionsTestRunner(unittest.TextTestRunner):
    '''
    classdocs
    '''
    def __init__(self, question_number, question_part):
        self.question_number = question_number
        self.question_part = question_part
        super(QuestionsTestRunner, self).__init__()

    def _makeResult(self):
        return QuestionsTextTestResult(self.question_number, self.question_part, self.stream, self.descriptions, self.verbosity)
