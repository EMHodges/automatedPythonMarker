import re
import sys

from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from django.shortcuts import render

from questions.models import QuestionComposite, SubQuestionComposite, TimeStarted
from results.models import Result, Subtest
from static_lint.models import StaticLint
from submission.models import Submission


def submit_page(request):
    context = {}
    return render(request, "submit_page/submit_page.html", context)

def submit_views(request):
    p = re.compile(r'(python-marker\d*).exe')
    z = p.search(sys.argv[0])

    print('yops')
    print(z)

    if z:
        filename = z.group(1)
    else:
        filename = 'pythonMarker'

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}.txt'

    lines = []

    questions = QuestionComposite.objects.all()

    for question in questions:
        subquestions = question.subquestioncomposite_set.all()

        lines.append(serialize(subquestions))
        lines.append(serialize(Result.objects.filter(question_number=question.number)))

        for result in Result.objects.filter(question_number=question.number):
                result_subtests = result.subtest_set.all()
                print(result_subtests)
                print(serialize(result_subtests))
                lines.append(serialize(result_subtests))
    print(lines)
    response.writelines(lines)

    return response





def submit_view(request):
    p = re.compile(r'(python-marker\d*).exe')
    z = p.search(sys.argv[0])

    if z:
        filename = z.group(1)
    else:
        filename = 'pythonMarker'

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}.txt'

    lines = []
    t = TimeStarted.objects.all()

    questions = QuestionComposite.objects.all()
    sub_questions = SubQuestionComposite.object.all()
    submissions = Submission.object.all()
    static_lint = StaticLint.objects.all()
    results = Result.objects.all()
    sub_tests = Subtest.objects.all()

    lines.append(serialize(t))
    lines.append(serialize(questions))
    lines.append(serialize(sub_questions))
    lines.append(serialize(submissions))
    lines.append(serialize(static_lint))
    lines.append(serialize(results))
    lines.append(serialize(sub_tests))

    response.writelines(lines)

    return response

def serialize(object):
    return serializers.serialize("yaml", object)