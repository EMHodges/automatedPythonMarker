import re

from django.core import serializers
from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from .forms import QuestionForm
from .models import Question, QuestionComposite, SubQuestionComposite
from results.main import run_tests, run_testing
from results.models import Result
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
    sub_obj = obj.subquestioncomposite_set.all()

    fords = {}

    for obj in sub_obj:
        fords[obj] = QuestionForm(None, instance=obj, prefix=int(obj.part))

    static_errors = StaticLint.objects.get_or_none(question_number=number)
    yo = {}

    if request.method == "POST":
        request_dict = request.POST.dict()
        for key, value in request_dict.items():
            answer_key = re.match(r'\d+-answer', key)
            if answer_key:
                first_letter = int(key[0])
                sub_question = SubQuestionComposite.objects.get(part=first_letter)
                form = QuestionForm(request.POST or None, instance=sub_question, prefix=str(first_letter))
                form_answer = request.POST.get(key)
                run_testing(form_answer, number, first_letter)
                if form.is_valid():
                    form.save()
                    x = get_object_or_404(QuestionComposite, number=number).subquestioncomposite_set.get(
                        part=first_letter)
                    fords.pop(sub_question)
                    fords[x] = form
                    run_testing(form_answer, number, first_letter)
                    static_errors = StaticLint.objects.get(question_number=number)

    yo[obj] = Result.objects.filter(question_number=1)
    print('resultzzz')
    print(yo)
    d = Result.objects.filter(question_number=4).all()
    print('resultz')
    for i in d:
        print(i.question_part)
        print(i.mark)
        print(i.test_feedback)
        print(i.test_result)
        print(i.test_name)
    context = {
        'form': fords,
        'next_question': None,
        'previous_question': None,
        'static_errors': static_errors,
        'test_results': yo,
        'mark': Result.objects.total_mark_for_question(question_number=number),
    }
    return render(request, "question/questions.html", context)


def question_list_view(request):
    queryset = Question.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "question/question_list.html", context)


def submit_view(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=submission.yaml'

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
