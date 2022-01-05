from django.db import models

# Create your models here.
from GetOrNoneManager import GetOrNoneManager


class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
    objects = GetOrNoneManager()
