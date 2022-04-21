import os

import yaml

from django.core.management.base import BaseCommand

from django.core import serializers


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('id', nargs="+", type=str)

    def handle(self, *args, **kwargs):
        id = kwargs['id'][0]

        fixture_file = os.path.join("data", id)
        with open(fixture_file) as stream:
            try:
                for obj in serializers.deserialize("yaml", stream):
                    obj.save()
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError as exc:
                print(f"Error creating object from file {fixture_file}")
                print(exc)

