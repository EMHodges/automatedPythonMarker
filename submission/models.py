from django.db import models

# Create your models here.
from GetOrNoneManager import GetOrNoneManager
from questions.models import SubQuestionComposite, SubQuestionCompositeManager


class SubmissionManager(GetOrNoneManager, models.Manager):

    def get_last_submission_number(self, sub_question: SubQuestionComposite):
        current_submission_number = self.all().filter(sub_question=sub_question)\
                                              .values_list('submission_number', flat=True)
        return max(current_submission_number) if current_submission_number else 0

    def get_last_submission(self, sub_question: SubQuestionComposite):
        submission_number = self.get_last_submission_number(sub_question)
        return self.get_or_none(sub_question=sub_question, submission_number=submission_number)

    def get_next_submission_number(self, sub_question: SubQuestionComposite):
        return self.get_last_submission_number(sub_question) + 1


class Submission(models.Model, models.Manager):
    sub_question = models.ForeignKey(SubQuestionComposite, on_delete=models.CASCADE)
    submission_number = models.IntegerField()
    submission_time = models.DateTimeField(auto_now=True)
    answer = models.TextField()
    object = SubmissionManager()


class TimeStarted(models.Model):
    time_started = models.DateTimeField(auto_now=True)
    objects = SubQuestionCompositeManager()
