import unittest
import re


class QuestionsTestCase(unittest.TestCase):
    '''
    classdocs
    '''

    def __init__(self, methodName='runTest', max_mark=None):
        self.max_mark = max_mark
        super(QuestionsTestCase, self).__init__(methodName)

        self.mark = 0

        print(self.max_mark)
        self.testMethodName = self._getTestMethodName()
        self.questionNumber = 1

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def _getTestMethodName(self):
        return self._testMethodName

    def setMark(self, mark):
        self.mark = mark

    def getMark(self):
        return self.mark
