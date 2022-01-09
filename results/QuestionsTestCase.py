import unittest


class QuestionsTestCase(unittest.TestCase):
    '''
    classdocs
    '''
    def __init__(self, methodName='runTest', max_mark=None):
        self.max_mark = max_mark
        super(QuestionsTestCase, self).__init__(methodName)

        self.mark = 0

        self.methodName = self._testMethodName
        self.questionNumber = 1

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def setMark(self, mark):
        self.mark = mark

    def getMark(self):
        return self.mark
