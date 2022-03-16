from django.db import models


# Create your models here.
from django.urls import reverse


class Question(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=True, null=True)
    max_mark = models.IntegerField()
    method_name = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("questions:question-update", kwargs={"number": self.number})


class QuestionComposite(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=False, null=False)


class SubQuestionComposite(models.Model):
    question = models.ForeignKey(QuestionComposite, on_delete=models.CASCADE)
    part = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    method_name = models.TextField()
    max_mark = models.IntegerField()
    answer = models.TextField(blank=True, null=True)
