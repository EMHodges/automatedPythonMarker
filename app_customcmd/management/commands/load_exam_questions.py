import os

from django.core import serializers
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path, dirs, files = next(os.walk("exam_questions"))
        for file in files:
            fixture_file = os.path.join("exam_questions", file)
            with open(fixture_file, 'r') as fixture:
                objects = serializers.deserialize('yaml', fixture)
                for obj in objects:
                    obj.save()