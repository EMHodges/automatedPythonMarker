from django.db import models

from GetOrNoneManager import GetOrNoneManager
from .resultsEnum import ResultsEnum


# Create your models here.
class Result(models.Model):
    question_number = models.IntegerField()
    test_name = models.TextField()
    test_result = models.CharField(max_length=10, choices=[(result, result.name) for result in ResultsEnum], default=ResultsEnum.ERROR)
    test_feedback = models.TextField()
    mark = models.IntegerField()
    objects = GetOrNoneManager()
