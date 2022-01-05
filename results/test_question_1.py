import unittest

from results import QuestionsTestCase
from static_lint.code_to_lint import calculateFine


class TestQuestion1(QuestionsTestCase.QuestionsTestCase):

    def testNoSpeed(self):
        """ Test that a value of 0 is returned when the speed is less than
        or equal to the speed limit.
        """
        self.assertAlmostEqual(0, calculateFine(50, 60), delta=0.000001)
        self.assertAlmostEqual(0, calculateFine(50, 50), delta=0.000001)
        self.assertAlmostEqual(0, calculateFine(70, 70), delta=0.000001)

    def testSpeedLower90(self):
        """ Test that fines are calculated correctly for speed below 90 mph.
        """
        self.assertAlmostEqual(150, calculateFine(60, 50), delta=0.000001)
        self.assertAlmostEqual(205, calculateFine(71, 50), delta=0.000001)
        self.assertAlmostEqual(200, calculateFine(70, 50), delta=0.000001)

    def testSpeedOver90(self):
        """ Test that fines are calculated correctly for speed of 90 mph or
        over. That is an additional penalty of 200 pounds should be added.
        """
        self.assertAlmostEqual(400, calculateFine(90, 70), delta=0.000001)
        self.assertAlmostEqual(505, calculateFine(91, 50), delta=0.000001)


if __name__ == '__main__':
    unittest.main()
