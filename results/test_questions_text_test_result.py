from django.test import TestCase

from results.models import Result
from results.questions_test_case import QuestionsTestCase
from results.questions_text_test_result import QuestionsTextTestResult
from results.results_enum import ResultsEnums


class QuestionsTextTestResultTestCase(TestCase):

    def test_sets_question_number_given_int(self):
        # Given
        question_number = 1

        # When
        questions_text_test_result = QuestionsTextTestResult(question_number=question_number)

        # Then
        self.assertEqual(questions_text_test_result.question_number, question_number)

    def test_sets_question_number_raises_exception_when_not_given_int(self):
        # Given
        question_number = 'one'

        # Then
        self.assertRaises(TypeError, QuestionsTextTestResult, question_number)

    def test_add_success_for_new_result(self):
        # Given
        questions_text_test_result = QuestionsTextTestResult(question_number=1)
        test = QuestionsTestCase(methodName='runTest')

        # When
        questions_text_test_result.addSuccess(test)
        result = Result.objects.get(question_number=1)

        # Then
        self.assertEqual(result.question_number, 1)
        self.assertEqual(result.test_result, ResultsEnums.SUCCESS)
        self.assertEqual(result.test_feedback, "Success")



