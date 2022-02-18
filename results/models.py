from django.db import models

from GetOrNoneManager import GetOrNoneManager

from .results_enum import ResultsEnums


class ResultManager(GetOrNoneManager, models.Manager):

    def update_or_creates(self, question_number, test_name, test_result, test_feedback, mark):
        self.update_or_create(question_number=question_number, test_name=test_name,
                              defaults={
                                  'test_feedback': test_feedback,
                                  'test_result': test_result,
                                  'mark': mark
                              })

    def total_mark_for_question(self, question_number):
        marks_for_question = self.filter(question_number=question_number).values_list('mark', flat=True)
        return sum(marks_for_question)

    def reset_mark(self, question_number, test_name):
        self.update_or_creates(question_number, test_name, ResultsEnums.SUCCESS, 'Bp', 0)


# Create your models here.
class Result(models.Model):
    question_number = models.IntegerField()
    test_name = models.TextField()
    test_result = models.CharField(max_length=2, choices=ResultsEnums.choices, default=ResultsEnums.SUCCESS)
    test_feedback = models.TextField()
    mark = models.IntegerField()
    objects = ResultManager()

    def update_test_result(self, result: ResultsEnums, feedback):
        self.test_result = ResultsEnums.get_yo(self.test_result, result)
        self.test_feedback = feedback
        self.save(update_fields=['test_result', 'test_feedback'])

    def get_failing_subtest_params(self):
        failing = self.subtest_set.exclude(test_result=ResultsEnums.SUCCESS)
        return [message for message in failing.values_list('params_failing', flat=True)]


class Subtest(models.Model):
    identifier = models.TextField()
    params_failing = models.TextField()
    test_result = models.CharField(max_length=2, choices=ResultsEnums.choices, default=ResultsEnums.ERROR)
    test = models.ForeignKey(Result, on_delete=models.CASCADE, null=True, blank=True)
