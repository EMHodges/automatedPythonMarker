import unittest
from .QuestionsTextTestResult import QuestionsTextTestResult


class QuestionsTestRunner(unittest.TextTestRunner):
    '''
    classdocs
    '''
    def __init__(self, question_number):
        self.question_number = question_number
        super(QuestionsTestRunner, self).__init__()

    def _makeResult(self):
        print('in here')
        return QuestionsTextTestResult(self.question_number, self.stream, self.descriptions, self.verbosity)
