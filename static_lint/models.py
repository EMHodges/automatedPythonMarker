from django.db import models

# Create your models here.
from GetOrNoneManager import GetOrNoneManager
from submission.models import Submission


class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    objects = GetOrNoneManager()
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, primary_key=True)
