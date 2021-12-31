from django.db import models


# Create your models here.
class Question(models.Model):
    number = models.IntegerField()
    description = models.TextField(blank=False, null=False)
    answer = models.TextField(blank=True, null=True)
    mark = models.DecimalField(decimal_places=3, max_digits=10, blank=True, default=0)
    max_mark = models.IntegerField()
    method_name = models.TextField(blank=True, null=True)
