import os

from django.core import serializers
from django.core.management.base import BaseCommand

from questions.models import Question

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        x = Question.objects.get(number=1)
        print(x)
        data = serializers.serialize("yaml", x)

        out = open("yo.yaml", "w")
        out.write(data)
        out.close()
