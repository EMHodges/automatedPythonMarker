from django.db import models

# Create your models here.
from django.urls import reverse

from GetOrNoneManager import GetOrNoneManager


class SubQuestionCompositeManager(GetOrNoneManager, models.Manager):
    pass


class QuestionComposite(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    objects = SubQuestionCompositeManager()

    def get_absolute_url(self):
        return reverse("questions:question-update", kwargs={"number": self.number})


class SubQuestionComposite(models.Model):
    question = models.ForeignKey(QuestionComposite, on_delete=models.CASCADE)
    part = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    method_name = models.TextField()
    max_mark = models.IntegerField()
    part_name = models.TextField(blank=False, null=False)
    object = SubQuestionCompositeManager()
