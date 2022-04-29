from unittest.mock import patch

from django.test import TestCase

from results.questions_test_case import QuestionsTestCase


class QuestionsTestCaseTestClass(TestCase):

    def test_mark_is_init_to_0(self):
        # Given

        # When
        question_test_case = QuestionsTestCase(methodName='runTest')

        # Then
        self.assertEqual(question_test_case.get_mark(), 0)

    @patch('results.questions_test_case')
    def test_set_mark(self, mocky):
        # Given
        mocky.__class__.__name__ = 'upup'
        mocky.__class__.__name__ = 'TestQuestion1'
        question_test_case = QuestionsTestCase(methodName='runTest')

        # When
        question_test_case.set_mark(20)

        # Then
        self.assertEqual(question_test_case.get_mark(), 20)