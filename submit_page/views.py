import re
import sys

from django.core import serializers
from django.http import HttpResponse

# Create your views here.
from questions.models import QuestionComposite
from results.models import Result


def submit_view(request):
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
        lines.append(serialize(Result.objects.filter(question_number=question.number)))

        for result in Result.objects.filter(question_number=question.number):
                result_subtests = result.subtest_set.all()
                lines.append(serialize(result_subtests) + '\n')

    response.writelines(lines)

    return response

def serialize(object):
    return serializers.serialize("yaml", object)