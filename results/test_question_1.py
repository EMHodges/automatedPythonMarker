import importlib
import unittest

import timeout_decorator

import static_lint.code_to_lint
from results import QuestionsTestCase
from results.main import setup_test

from static_lint.code_to_lint import calculateFine

# Todo error when run in exe it's not picking up import or syntax errors, also if you write the correct code and then
# change the name of the function it will still show that the result is correct
class TestQuestion1(QuestionsTestCase.QuestionsTestCase):

    def setUp(self) -> None:
        importlib.reload(static_lint.code_to_lint)

    @setup_test(max_mark=6)
    def testNoSpee(self):
        from static_lint.code_to_lint import calculateFine
        """ Test that a value of 0 is returned when the speed is less than
        or equal to the speed limit.
        """
        self.assertAlmostEqual(0, calculateFine(50, 60), delta=0.000001)
        self.assertAlmostEqual(0, calculateFine(50, 50), delta=0.000001)
        self.assertAlmostEqual(0, calculateFine(70, 70), delta=0.000001)

    @setup_test(max_mark=6)
    def testSpeedLower90(self):
        from static_lint.code_to_lint import calculateFine
        """ Test that fines are calculated correctly for speed below 90 mph.
        """
        self.assertAlmostEqual(150, calculateFine(60, 50), delta=0.000001)
        self.assertAlmostEqual(205, calculateFine(71, 50), delta=0.000001)
        self.assertAlmostEqual(200, calculateFine(70, 50), delta=0.000001)

    @setup_test(max_mark=6)
    def testSpeedOver90(self):
        from static_lint.code_to_lint import calculateFine
        """ Test that fines are calculated correctly for speed of 90 mph or
        over. That is an additional penalty of 200 pounds should be added.
        """
        self.assertAlmostEqual(400, calculateFine(90, 70), delta=0.000001)
        self.assertAlmostEqual(505, calculateFine(91, 50), delta=0.000001)


if __name__ == '__main__':
    unittest.main()