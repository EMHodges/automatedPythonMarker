from django.db import models

# Create your models here.
from GetOrNoneManager import GetOrNoneManager
from questions.models import SubQuestionComposite


class SubmissionManager(GetOrNoneManager, models.Manager):

    def get_last_submission_number(self, sub_question: SubQuestionComposite):
        current_submission_number = self.all().filter(sub_question=sub_question).values_list('submission_number', flat=True)
      #  value = current_submission_number ? max(current_submission_number) : 0
        return max(current_submission_number) if current_submission_number else 0
       # return current_submission_number ? max(self.all().filter(sub_question=sub_question).values_list('submission_number', flat=True))

    def get_last_submission(self, sub_question: SubQuestionComposite) -> SubQuestionComposite:
        submission_number = self.get_last_submission_number(sub_question)
        return self.get_or_none(sub_question=sub_question, submission_number=submission_number)

    def get_next_submission_number(self, sub_question: SubQuestionComposite):
        return self.get_last_submission_number(sub_question) + 1


class Submission(models.Model, models.Manager):
    sub_question = models.ForeignKey(SubQuestionComposite, on_delete=models.CASCADE)
    submission_number = models.IntegerField()
    submission_time = models.DateTimeField(auto_now=True)
    object = SubmissionManager()
