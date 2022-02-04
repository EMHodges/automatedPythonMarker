import unittest

from results.new_file import RegisterTestClass
from results.questions_test_case import QuestionsTestCase
from configs.utils.test_case_parameters import TestCaseParameter
from results.utils import setup_test, setup


@RegisterTestClass(question_number=1)
class TestQuestion1(QuestionsTestCase):

    @setup(max_mark=6, test_params=[
        TestCaseParameter(inputs={'a': 0, 'b': 0}, result=0, msg="hi"),
        TestCaseParameter(inputs={'a': 0, 'b': 0}, result=0, msg="hi2"),
    ])
    def testNoSpeed(self, test_param: TestCaseParameter):
        from static_lint.code_to_lint import calculateFine
        """ Test that a value of 0 is returned when the speed is less than
        or equal to the speed limit.
        """
        self.expectAlmostEqual(test_param.result, calculateFine(test_param.inputs['a'], test_param.inputs['b']), delta=0.000001, msg=test_param.message)

    @setup_test(max_mark=6)
    def testSpeedLower90(self):
        from static_lint.code_to_lint import calculateFine
        """ Test that fines are calculated correctly for speed below 90 mph.
        """
        self.expectAlmostEqual(150, calculateFine(60, 50), delta=0.000001, msg='60, 50')
        self.expectAlmostEqual(205, calculateFine(71, 50), delta=0.000001, msg='71, 50')

    @setup_test(max_mark=6)
    def testSpeedOver90(self):
        from static_lint.code_to_lint import calculateFine
        """ Test that fines are calculated correctly for speed of 90 mph or
        over. That is an additional penalty of 200 pounds should be added.
        """
        self.expectAlmostEqual(400, calculateFine(90, 70), delta=0.000001, msg='90, 70')
        self.expectAlmostEqual(505, calculateFine(91, 50), delta=0.000001, msg='91, 50')


if __name__ == '__main__':
    unittest.main()
