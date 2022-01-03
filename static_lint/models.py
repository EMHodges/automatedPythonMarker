from django.db import models


<<<<<<< HEAD
# Create your models here.
from django.urls import reverse


class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField(blank=True, null=True)
=======
class StaticLint(models.Model):
    question_number = models.IntegerField()
    feedback = models.TextField()
>>>>>>> 32b5e96 (adding static lint display)
