import os
import re
from typing import Dict, List

import yaml

from django.core.management.base import BaseCommand
from questions.models import Question, QuestionComposite, SubQuestionComposite
from collections import defaultdict

from results.models import Result

def question_update_view(request, number):
    obj = get_object_or_404(Question, id=number)
    obj2 = get_object_or_404(Question, id=2)
    form = QuestionForm(None, instance=obj, prefix=int(number))
    form2 = QuestionForm(None, instance=obj2, prefix=int(number)+1)

    next_question = Question.objects.filter(number__gt=obj.number).order_by('number').first()
    previous_question = Question.objects.filter(number__lt=obj.number).order_by('number').last()

    static_errors = StaticLint.objects.get_or_none(question_number=number)
    yo = {}

    if request.method == "POST" and request.POST.get('1-answer'):
        form = QuestionForm(request.POST or None, instance=obj, prefix='1')
        form_answer = request.POST.get('1-answer')
        run_tests(form_answer, 1)
        static_errors = StaticLint.objects.get(question_number=1)
        if form.is_valid():
            form.save()

    if request.method == "POST" and request.POST.get('2-answer'):
        form2 = QuestionForm(request.POST or None, instance=obj2, prefix='2')

        form_answer = request.POST.get('2-answer')
        run_tests(form_answer, 2)
        static_errors = StaticLint.objects.get(question_number=2)
        if form2.is_valid():
            form2.save()

    yo[obj] = Result.objects.filter(question_number=1)
    yo[obj2] = Result.objects.filter(question_number=2)
    forms = {obj: form, obj2: form2}

    context = {
        'form': forms,
        'next_question': next_question,
        'previous_question': previous_question,
        'static_errors': static_errors,
        'test_results': yo,
        'mark': Result.objects.total_mark_for_question(question_number=number),
    }
    return render(request, "question/question.html", context)






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
        comp_files = self._get_comp_files(config_files)
        print(question_files)
        print(comp_files)
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

        QuestionComposite.objects.all().delete()
        print('deleted questions')

        for question in questions:
            QuestionComposite.save(question)

        for file in comp_files:
            x = self._load_part_question(file)
            SubQuestionComposite.save(x)
            print(SubQuestionComposite.objects.all())

    def _load_question(self, file: str) -> Question:
        fixture_file = os.path.join("configs", file)
        print(fixture_file)
        with open(fixture_file) as stream:
            try:
                question_values = yaml.safe_load(stream)
                print(question_values)
                question = QuestionComposite(**question_values)
                # self._set_defaults(question)
                return question
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError as exc:
                print(f"Error creating object from file {fixture_file}")
                print(exc)

    def _load_part_question(self, file: str) -> SubQuestionComposite:
        fixture_file = os.path.join("configs", file)
        print(fixture_file)

        with open(fixture_file) as stream:
            try:
                question_values = yaml.safe_load(stream)
                print(question_values)
                q = QuestionComposite.objects.get(number=question_values['number'])
                question_values['question'] = q
                question_values.pop('number')
                question = SubQuestionComposite(**question_values)
                print(question)
                # self._set_defaults(question)
                return question
            except yaml.YAMLError as exc:
                print(exc)
            except TypeError as exc:
                print(f"Error creating object from file {fixture_file}")
                print(exc)

    @staticmethod
    def _get_question_files(config_files):
        return [file for file in config_files if re.match(r't_question_\d+.yaml', file)]

    @staticmethod
    def _get_comp_files(config_files):
        return [file for file in config_files if re.match(r't_question_\d+\w+.yaml', file)]

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
