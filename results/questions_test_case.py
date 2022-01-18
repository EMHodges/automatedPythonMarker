import unittest


class QuestionsTestCase(unittest.TestCase):
    '''
    classdocs
    '''
    def __init__(self, methodName='runTest'):
        super(QuestionsTestCase, self).__init__(methodName)
        self._mark = 0
        self.methodName = self._testMethodName

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def setMark(self, mark):
        self._mark = mark

    def getMark(self):
        return self._mark
