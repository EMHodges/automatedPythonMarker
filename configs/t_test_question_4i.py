import unittest

from results.new_file import RegisterTestClass, RegisterCompositeTestClass
from results.questions_test_case import QuestionsTestCase
from results.utils import setup_test


@RegisterCompositeTestClass(question_number=4, question_part=1)
class TestQuestion4i(QuestionsTestCase):

    @setup_test(max_mark=6)
    def testquestion4i(self):
        from static_lint.code_to_lint import yoyo
        """ Test that a value of 0 is returned when the speed is less than
        or equal to the speed limit.
        """
        self.expectAlmostEqual(1, yoyo(0,0,0), delta=0.000001, msg='0, 0')

    @setup_test(max_mark=6)
    def testSpeedLower90(self):
        from static_lint.code_to_lint import yoyo
        """ Test that fines are calculated correctly for speed below 90 mph.
        """
        self.expectAlmostEqual(0, yoyo(0, 1, 0), delta=0.000001, msg='71, 50')

    @setup_test(max_mark=6)
    def testSpeedOver90(self):
        from static_lint.code_to_lint import yoyo
        """ Test that fines are calculated correctly for speed of 90 mph or
        over. That is an additional penalty of 200 pounds should be added.
        """
        self.expectAlmostEqual(0, yoyo(0, 1, 0), delta=0.000001, msg='71, 50')


if __name__ == '__main__':
    unittest.main()

