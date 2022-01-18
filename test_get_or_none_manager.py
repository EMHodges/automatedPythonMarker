from django.test import TestCase
from results.models import Result
from results.results_enum import ResultsEnums


class GetOrNoneManagerTestCase(TestCase):

    def test_get_or_none_returns_object_when_object_exists(self):
        # Given
        result = Result(question_number=1, test_name='test', test_result=ResultsEnums.SUCCESS,
                        test_feedback='feedback', mark=1)
        result.save()

        # When
        result_db = Result.objects.get_or_none(question_number=1)  # Can be any object that extends GetOrNoneManager

        # Then
        self.assertEqual(result, result_db)

    def test_get_or_none_returns_none_when_model_does_not_exist(self):
        # Given

        # When
        result = Result.objects.get_or_none(question_number=1)

        # Then
        self.assertEqual(result, None)
