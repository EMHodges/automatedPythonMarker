import re
import sys
from io import StringIO

from django.core import serializers
from django.core.handlers.wsgi import WSGIRequest
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

    run_all_tests()

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

def run_all_tests():
    pass

def fake_post_request(method=None, fake_user=False):
    '''Returns a fake `WSGIRequest` object that can be passed to viewss.
    If `fake_user` is `True`, we attach a random staff member to the request.
    Even if not set, you can still do this manually by setting the `user`
    attribute on the returned object.
    The `GET` and `POST` `QueryDict` objects are mutable::
        req = fake_request(mutable=True)
        req.GET['q'] = 'abc'
        my_view(req)
    '''
    request = WSGIRequest({
        'REQUEST_METHOD': method or 'GET',
        'wsgi.input': StringIO(),
    })
    return request