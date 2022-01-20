from django.db import models

from GetOrNoneManager import GetOrNoneManager
from .new_file import RegisterTestClass

from .results_enum import ResultsEnums


class ResultManager(GetOrNoneManager, models.Manager):

    def error_tests(self, question_number, reason):
        test_names = RegisterTestClass.test_method_names_for_question[question_number]
        for test_name in test_names:
            self.update_or_creates(question_number, test_name, ResultsEnums.ERROR, reason, 0)

    def update_or_creates(self, question_number, test_name, test_result, test_feedback, mark):
        self.update_or_create(question_number=question_number, test_name=test_name,
                              defaults={
                                  'test_result': test_result,
                                  'test_feedback': test_feedback,
                                  'mark': mark
                              })

    def total_mark_for_question(self, question_number):
        marks_for_question = self.filter(question_number=question_number).values_list('mark', flat=True)
        return sum(marks_for_question)


# Create your models here.
class Result(models.Model):
    question_number = models.IntegerField()
    test_name = models.TextField()
    test_result = models.CharField(max_length=2, choices=ResultsEnums.choices, default=ResultsEnums.ERROR)
    test_feedback = models.TextField()
    mark = models.IntegerField()
    objects = ResultManager()
