from django.test import TestCase

from results.questions_test_case import QuestionsTestCase


class QuestionsTestCaseTestClass(TestCase):

    def test_mark_is_init_to_0(self):
        # Given

        # When
        question_test_case = QuestionsTestCase(methodName='runTest')

        # Then
        self.assertEqual(question_test_case.getMark(), 0)

    def test_set_mark(self):
        # Given
        question_test_case = QuestionsTestCase(methodName='runTest')

        # When
        question_test_case.setMark(20)

        # Then
        self.assertEqual(question_test_case.getMark(), 20)