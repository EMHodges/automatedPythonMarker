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


def submit_view(request):
    p = re.compile(r'(python-marker\d{6}).exe')
    mac = re.compile(r'(python-marker\d{6})')

    filename = 'python-marker'
    for arg in sys.argv:
        match = p.search(arg)
        if match:
            filename = match.group(1)
    if filename == 'python-marker':
        for arg in sys.argv:
            match = mac.search(arg)
            if match:
                filename = match.group(1)

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
