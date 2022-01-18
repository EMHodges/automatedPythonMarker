from django.test import TestCase

from results.models import Result
from results.results_enum import ResultsEnums


class ResultManagerTestCase(TestCase):

    def test_result_is_created_when_result_does_not_exist(self):
        # Given
        question_number = 1
        test_name = 'test'

        # When
        Result.objects.update_or_creates(question_number=question_number, test_name=test_name,
                                         test_result=ResultsEnums.FAIL, test_feedback='error',
                                         mark=0)
        result = Result.objects.get(question_number=1)

        # Then
        self.assertEqual(result.mark, 0)
        self.assertEqual(result.test_feedback, 'error')

    def test_result_is_updated_when_result_exists(self):
        # Given
        question_number = 1
        test_name = 'test'

        Result.objects.create(question_number=question_number, test_name=test_name,
                              test_result=ResultsEnums.SUCCESS, test_feedback='feedback', mark=3)

        # When
        Result.objects.update_or_creates(question_number=question_number, test_name=test_name,
                                         test_result=ResultsEnums.FAIL, test_feedback='error',
                                         mark=0)
        result = Result.objects.get(question_number=1)

        # Then
        self.assertEqual(result.mark, 0)
        self.assertEqual(result.test_feedback, 'error')
