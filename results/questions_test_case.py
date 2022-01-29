import importlib
import random
import unittest

from results.new_file import RegisterTestClass


class QuestionsTestCase(unittest.TestCase):
    '''
    classdocs
    '''
    def __init__(self, methodName='runTest'):
        super(QuestionsTestCase, self).__init__(methodName)
        self._mark = 0
        self.methodName = self._testMethodName
        self._questionNumber = self._get_question_number()

    def __call__(self, *args, **kwds):
        return self.run(*args, **kwds)

    def setUp(self) -> None:
        import static_lint.code_to_lint
        importlib.reload(static_lint.code_to_lint)

    def set_mark(self, mark):
        self._mark = mark

    def get_mark(self):
        return self._mark

    def get_question_number(self):
        return self._questionNumber

    def _get_question_number(self):
        return RegisterTestClass.get_test_question_number(self.methodName)

    # ToDo override all of these methods add message which includes the input of the
    # function so that this can be outputted, maybe add mark here?
    def expectEqual(self, first, second, msg=None):
        with self.subTest():
            self.assertEqual(first, second, msg)

    def expectAlmostEqual(self, first, second, places=None, msg=None,
                          delta=None):
        g = random.randint(0, 909090)
        with self.subTest(msg=g):
            print('new sub test')
            self.assertAlmostEqual(first, second, places=places, msg=msg,
                          delta=delta)
            self.set_mark(4)
