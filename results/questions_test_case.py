import importlib
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

    def expectTrue(self, expr, msg):
        with self.subTest(msg=msg):
            super().assertTrue(expr, msg=msg)

    def expectFalse(self, expr, msg):
        with self.subTest(msg=msg):
            super().assertFalse(expr, msg=msg)

    def expectRaises(self,expected_exception, msg, *args, **kwargs):
        with self.subTest(msg=msg):
            super().assertRaises(expected_exception, *args, **kwargs)

    def expectWarns(self, expected_warning, msg, *args, **kwargs):
        with self.subTest(msg=msg):
            super().assertWarns(expected_warning, *args, **kwargs)

    # ToDo override all of these methods add message which includes the input of the
    # function so that this can be outputted, maybe add mark here?
    def expectEqual(self, first, second, msg):
        with self.subTest(msg=msg):
            super().assertEqual(first, second, msg)

    def expectNotEqual(self, first, second, msg):
        with self.subTest(msg=msg):
            super().assertNotEqual(first, second, msg)

    def expectAlmostEqual(self, first, second, msg, places=None, delta=None):
        with self.subTest(msg=msg):
            super().assertAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    def expectNotAlmostEqual(self, first, second, msg, places=None, delta=None):
        with self.subTest(msg=msg):
            super().assertNotAlmostEqual(first, second, places=places, msg=msg, delta=delta)

    def expectListEqual(self, list1, list2, msg):
        with self.subTest(msg=msg):
            super().assertListEqual(list1, list2, msg)
