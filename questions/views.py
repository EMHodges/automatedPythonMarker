from django.core import serializers
from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from .forms import QuestionForm
from .models import Question
from results.main import run_tests
from results.models import Result
from django.http import HttpResponse


# Create your views here.
def question_update_view(request, number):
    obj = get_object_or_404(Question, id=number)
    obj2 = get_object_or_404(Question, id=2)
    form = QuestionForm(request.POST or None, instance=obj, prefix='1')
    form2 = QuestionForm(request.POST or None, instance=obj2, prefix='2')
    forms = {obj: form, obj2: form2}
    question = Question.objects.get(number=number)
    next_question = Question.objects.filter(number__gt=obj.number).order_by('number').first()
    previous_question = Question.objects.filter(number__lt=obj.number).order_by('number').last()

    static_errors = StaticLint.objects.get_or_none(question_number=number)
    test_results = Result.objects.filter(question_number=number)
    yo = {}
    questions = [question, Question.objects.get(number=2)]
    for obg, form in forms.items():
        print(obg)
        print(form)
        if form.is_valid():
            form.save()
    print('POSTY')
    print(request.POST.get('3-answer'))
    if request.method == "POST" and request.POST.get('1-answer'):
        print('1-answer')
        form_answer = request.POST.get('1-answer')
        run_tests(form_answer, 1)
        static_errors = StaticLint.objects.get(question_number=1)
        test_results = Result.objects.filter(question_number=1)

    if request.method == "POST" and request.POST.get('2-answer'):
        print('2-answer')
        form_answer = request.POST.get('2-answer')
        run_tests(form_answer, 2)
        static_errors = StaticLint.objects.get(question_number=2)
        test_results = Result.objects.filter(question_number=2)
        yo[obj] = Result.objects.filter(question_number=2)

    yo[obj] = Result.objects.filter(question_number=1)
    yo[obj2] = Result.objects.filter(question_number=2)

    print('RESULTS')
    print(Result.objects.filter(question_number=1))
    print(Result.objects.filter(question_number=2))
    print(test_results)
    print('yops')
    print(yo)
    context = {
        'form': forms,
        'object': obj,
        'next_question': next_question,
        'previous_question': previous_question,
        'static_errors': static_errors,
        'test_results': yo,
        'question': questions,
        'mark': Result.objects.total_mark_for_question(question_number=number),
    }
    return render(request, "question/question.html", context)


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
