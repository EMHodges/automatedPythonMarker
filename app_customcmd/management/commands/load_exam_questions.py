import os
from typing import Dict, List

import yaml

from django.core.management.base import BaseCommand
from questions.models import Question
from collections import defaultdict


class DuplicateQuestionNumberException(Exception):
    """Raise for my specific kind of exception"""

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
        path, dirs, question_files = next(os.walk("exam_questions"))
        questions = []
        question_numbers = defaultdict(list)

        for file in question_files:
            question = self._load_question(file)
            questions.append(question)
            question_numbers[question.number].append(file)

        self._validate_question_numbers(question_numbers)

        Question.objects.all().delete()
        for question in questions:
            Question.save(question)

    @staticmethod
    def _load_question(file: str) -> Question | None:
        fixture_file = os.path.join("exam_questions", file)

        with open(fixture_file) as stream:
            try:
                question_values = yaml.safe_load(stream)
                question = Question(**question_values)
                Command._set_defaults(question)
                return question
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError as exc:
                print(f"Error creating object from file {fixture_file}")
                print(exc)

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
