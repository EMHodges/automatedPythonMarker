import os
import re
from typing import Dict, List

import yaml

from django.core.management.base import BaseCommand
from questions.models import QuestionComposite, SubQuestionComposite
from collections import defaultdict

from results.models import Result
from django.core import serializers


class DuplicateQuestionNumberException(Exception):
    """Raise when multiple question files have the same question number"""

    def __init__(self, error):
        self.error = error
        self.message = self._create_error_message(error)
        super().__init__(self.message)

    @staticmethod
    def _create_error_message(error):
        error_message = ["Question numbers must be unique \n"]
        for question_number, file_paths in error.items():
            file_paths = ', '.join(file_paths)
            error_message.append(f"The files: \"{file_paths}\" define questions with question number {question_number} "
                                 f"\n")
        return ''.join(error_message)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        path, dirs, config_files = next(os.walk("configs"))

        submission_files = self._get_submission_files(config_files)



        for file in submission_files:
            fixture_file = os.path.join("configs", file)
            with open(fixture_file) as stream:
                try:
                    for obj in serializers.deserialize("yaml", stream):
                        obj.save()
                except yaml.YAMLError as exc:
                    print(exc)
                except TypeError as exc:
                    print(f"Error creating object from file {fixture_file}")
                    print(exc)

    @staticmethod
    def _get_submission_files(config_files):
        return [file for file in config_files if re.match(r'submission.yaml', file)]

