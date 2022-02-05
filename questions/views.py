from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from .forms import QuestionForm
from .models import Question
from results.main import run_tests
from results.models import Result


# Create your views here.
def question_update_view(request, number):
    obj = get_object_or_404(Question, id=number)
    form = QuestionForm(request.POST or None, instance=obj)

    question = Question.objects.get(number=number)
    next_question = Question.objects.filter(number__gt=obj.number).order_by('number').first()
    previous_question = Question.objects.filter(number__lt=obj.number).order_by('number').last()

    static_errors = StaticLint.objects.get_or_none(question_number=number)
    test_results = Result.objects.filter(question_number=number)

    if form.is_valid():
        form.save()

    # Todo make it only run the tests if there are no syntax errors
    if request.method == "POST":
        form_answer = request.POST.get("answer")
        run_tests(form_answer, number)
        static_errors = StaticLint.objects.get(question_number=number)
        test_results = Result.objects.filter(question_number=number)

    r = []
    g = Result.objects.filter(question_number=number)
    for i in g:
        x = i.subtest_set.all().values_list('message', flat=True)
        for c in x:
            r.append(c)
    print(r)

    context = {
        'form': form,
        'object': obj,
        'next_question': next_question,
        'previous_question': previous_question,
        'static_errors': static_errors,
        'test_results': test_results,
        'mark': Result.objects.total_mark_for_question(question_number=number),
        'subtest': r,
        'question': question
    }
    return render(request, "question/question.html", context)


def question_list_view(request):
    queryset = Question.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "question/question_list.html", context)
