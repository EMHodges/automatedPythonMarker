from django.db import models

# Create your models here.


class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
