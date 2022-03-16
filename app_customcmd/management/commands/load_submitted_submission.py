import os

import yaml

from django.core.management.base import BaseCommand

from django.core import serializers


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path, dirs, submission_files = next(os.walk("data"))
        print(submission_files)


        for file in submission_files:
            fixture_file = os.path.join("data", file)
            print(fixture_file)
            with open(fixture_file) as stream:
                try:
                    for obj in serializers.deserialize("yaml", stream):
                        obj.save()
                except yaml.YAMLError as exc:
                    print(exc)
                except TypeError as exc:
                    print(f"Error creating object from file {fixture_file}")
                    print(exc)

