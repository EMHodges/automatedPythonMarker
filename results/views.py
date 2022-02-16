from django.shortcuts import render

from questions.models import Question
from results.models import Result


def results_page_view(request):
    queryset = Result.objects.all().order_by('question_number')
    mark_questions = {}
    results_dict = {}
    max_mark = {}

    for i in queryset:
        results_dict.setdefault(i.question_number, []).append(i)

    for question in Question.objects.all():
        mark_questions[question.number] = Result.objects.total_mark_for_question(question_number=question.number)
        max_mark[question.number] = question

    context = {
        "test_result": results_dict,
        "mark_questions": mark_questions,
        "max_mark": max_mark,
    }

    return render(request, "results.html", context)
