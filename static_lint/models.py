from django.db import models


# Create your models here.
from django.urls import reverse


class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
