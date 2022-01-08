import ast

from django.db import models

from GetOrNoneManager import GetOrNoneManager
from .utils import extractTestNames
from .resultsEnum import ResultsEnum


# Create your models here.
class Result(models.Model):
    question_number = models.IntegerField()
    test_name = models.TextField()
    test_result = models.CharField(max_length=10, choices=[(result, result.name) for result in ResultsEnum],
                                   default=ResultsEnum.ERROR)
    test_feedback = models.TextField()
    mark = models.IntegerField()
    objects = GetOrNoneManager()

    @classmethod
    def error_tests_for_question(cls, question_number, reason):
        test_names = extractTestNames(question_number)
        for test_name in test_names:
            cls.objects.update_or_create(question_number=question_number, test_name=test_name,
                                         defaults={
                                             'test_result': ResultsEnum.ERROR,
                                             'test_feedback': reason,
                                             'mark': 0
                                         })

