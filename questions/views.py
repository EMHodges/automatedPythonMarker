import os
import re
import sys
from pathlib import Path

from django.core import serializers
from django.shortcuts import render, get_object_or_404

from automatedPythonMarker.settings import resource_path, yo
from static_lint.models import StaticLint
from .forms import QuestionForm
from .models import Question, QuestionComposite, SubQuestionComposite
from results.main import run_tests, run_testing
from results.models import Result, Subtest
from django.http import HttpResponse


# Create your views here.
def question_update_view(request, number):
    obj = get_object_or_404(Question, id=number)
    obj2 = get_object_or_404(Question, id=2)
    form = QuestionForm(None, instance=obj, prefix=int(number))
    form2 = QuestionForm(None, instance=obj2, prefix=int(number) + 1)

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


def question_update_views(request, number):
    obj = get_object_or_404(QuestionComposite, number=number)
    print(obj)
    print('sys')
    print(sys.executable)
    print(sys.argv)

    sub_objs = obj.subquestioncomposite_set.all()

    fords = {}

    static_errors = StaticLint.objects.get_or_none(question_number=number)
    yo = {}

    if request.method == "POST":
        request_dict = request.POST.dict()
        for key, value in request_dict.items():
            answer_key = re.match(r'\d+-answer', key)
            if answer_key:
                first_letter = int(key[0])

                for sub_obj in sub_objs:
                    if first_letter == sub_obj.part:
                        sub_question = SubQuestionComposite.objects.get(part=first_letter)
                        form = QuestionForm(request.POST or None, instance=sub_question, prefix=str(first_letter))
                        form_answer = request.POST.get(key)

                        if form.is_valid():
                            form.save()
                            x = get_object_or_404(QuestionComposite, number=number).subquestioncomposite_set.get(
                                part=first_letter)
                            fords[x] = form
                            run_testing(form_answer, number, first_letter)
                            static_errors = StaticLint.objects.get(question_number=number)
                    else:
                        fords[sub_obj] = QuestionForm(None, instance=sub_obj, prefix=int(sub_obj.part))
    else:
        for objz in sub_objs:
            fords[objz] = QuestionForm(None, instance=objz, prefix=int(objz.part))

    for objz in sub_objs:
        yo[objz] = Result.objects.filter(question_number=number, question_part=objz.part)
    context = {
        'form': fords,
        'next_question': None,
        'previous_question': None,
        'static_errors': static_errors,
        'test_results': yo,
        'question': obj,
        'mark': Result.objects.total_mark_for_question(question_number=number),
    }
    print(Path(__file__).stem)
    return render(request, "question/questions.html", context)


def question_list_view(request):
    queryset = Question.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "question/question_list.html", context)

def submit_view(request):
    p = re.compile(r'(python-marker\d*).exe')
    z = p.search(sys.argv[0])

    print('yops')
    print(yo)
    print(z)

    if z:
        filename = z.group(1)
    else:
        filename = 'pythonMarker'

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}.txt'


    lines = []

    questions = QuestionComposite.objects.all()
    print(questions)

    for question in questions:
        subquestions = question.subquestioncomposite_set.all()

        lines.append(serialize(subquestions))
        lines.append(serialize(Result.objects.filter(question_number=question.number)))
        lines.append(serialize(Result.objects.filter(question_number=question.number)))

        for result in Result.objects.filter(question_number=question.number):
                result_subtests = result.subtest_set.all()
                lines.append(serialize(result_subtests) + '\n')

    response.writelines(lines)

    return response


def serialize(object):
    return serializers.serialize("yaml", object)

def submit_views(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=submissio.txt'

    lines = []

    questions = Question.objects.all()

    for question in questions:
        lines.append(f'question-number: {question.number} \n')
        lines.append(question.answer)
        lines.append('\n')
        lines.append('\n')
    response.writelines(lines)

    data = serializers.serialize("yaml", Question.objects.all())
    response.writelines(data)
    return response
