import os
import re
from typing import Dict, List

import yaml

from django.core.management.base import BaseCommand
from questions.models import Question
from collections import defaultdict

from results.models import Result


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

        question_files = self._get_question_files(config_files)
        questions = []
        question_numbers = defaultdict(list)

        for file in question_files:
            question = self._load_question(file)
            questions.append(question)
            question_numbers[question.number].append(file)

        self._validate_question_numbers(question_numbers)
        print(questions)
        Result.objects.all().delete()
        print('deleted results')

        Question.objects.all().delete()
        print('deleted questions')

        for question in questions:
            Question.save(question)

    def _load_question(self, file: str) -> Question:
        fixture_file = os.path.join("configs", file)

        with open(fixture_file) as stream:
            try:
                question_values = yaml.safe_load(stream)
                question = Question(**question_values)
                self._set_defaults(question)
                return question
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError as exc:
                print(f"Error creating object from file {fixture_file}")
                print(exc)

    @staticmethod
    def _get_question_files(config_files):
        return [file for file in config_files if re.match(r'question_\d*.yaml', file)]

    @staticmethod
    def _set_defaults(question: Question) -> None:
        question.pk = question.number
        question.mark = 0
        question.answer = None

    @staticmethod
    def _validate_question_numbers(question_numbers: Dict[int, List[str]]) -> None or DuplicateQuestionNumberException:
        duplicate_question_numbers = {}

        for question_number, question_path in question_numbers.items():
            is_question_number_duplicated = len(question_path) > 1
            if is_question_number_duplicated:
                duplicate_question_numbers[question_number] = question_path

        if duplicate_question_numbers:
            raise DuplicateQuestionNumberException(duplicate_question_numbers)
