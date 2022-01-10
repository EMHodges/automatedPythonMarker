from django.db import models

from GetOrNoneManager import GetOrNoneManager
from .utils import extractTestNames
from .results_enum import ResultsEnum


class ResultManager(GetOrNoneManager, models.Manager):

    def error_tests_for_question(self, question_number, reason):
        test_names = extractTestNames(question_number)
        for test_name in test_names:
            self.update_or_creates(question_number, test_name, ResultsEnum.ERROR, reason, 0)

    def update_or_creates(self, question_number, test_name, test_result, test_feedback, mark):
        self.update_or_create(question_number=question_number, test_name=test_name,
                              defaults={
                                  'test_result': test_result,
                                  'test_feedback': test_feedback,
                                  'mark': mark
                              })


# Create your models here.
class Result(models.Model):
    question_number = models.IntegerField()
    test_name = models.TextField()
    test_result = models.CharField(max_length=10, choices=[(result, result.name) for result in ResultsEnum],
                                   default=ResultsEnum.ERROR)
    test_feedback = models.TextField()
    mark = models.IntegerField()
    objects = ResultManager()
