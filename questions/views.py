import re
import sys

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from submission.models import Submission
from submission.forms import QuestionForm
from .models import Question, QuestionComposite, SubQuestionComposite, TimeStarted
from results.main import run_testing, create_submission
from results.models import Result, Subtest
from django.core import serializers


# Create your views here.
def question_update_views(request, number):
    obj = get_object_or_404(QuestionComposite, number=number)
    print("update views!")
    sub_objs = obj.subquestioncomposite_set.all()

    time_obj = TimeStarted.objects.get_or_none()
    if not time_obj:
        time = TimeStarted()
        time.save()

    fords = {}

    yo = {}
    static_error = {}

    if request.method == "POST":
        request_dict = request.POST.dict()
        print(request.POST.dict())
        for key, value in request_dict.items():
            answer_key = re.match(r'\d+-answer', key)
            if answer_key:
                first_letter = int(key[0])

                for sub_obj in sub_objs:
                    if first_letter == sub_obj.part:
                        submission = create_submission(number, first_letter)
                        # sub_question = SubQuestionComposite.object.get(part=first_letter)
                        form = QuestionForm(request.POST or None, instance=submission, prefix=str(first_letter))
                        form_answer = request.POST.get(key)

                        if form.is_valid():
                            form.save()
                            x = get_object_or_404(QuestionComposite, number=number).subquestioncomposite_set.get(
                                part=first_letter)
                            fords[x] = form
                            run_testing(form_answer, number, first_letter, submission)
                            # static_errors = StaticLint.objects.get(question_number=number)
                    else:
                        submission = Submission.object.get_last_submission(sub_obj)
                        fords[sub_obj] = QuestionForm(None, instance=submission, prefix=int(sub_obj.part))
    else:
        for objz in sub_objs:
            submission = Submission.object.get_last_submission(objz)
            fords[objz] = QuestionForm(None, instance=submission, prefix=int(objz.part))

    for objz in sub_objs:
        last_submission = Submission.object.get_last_submission(objz)
        if (hasattr(last_submission, 'staticlint')):
            static_error[objz] = last_submission.staticlint
        else:
            static_error[objz] = None
        yo[objz] = Result.objects.filter(question_number=number, question_part=objz.part, submission=last_submission)
    print(static_error)
    context = {
        'form': fords,
        'next_question': None,
        'previous_question': None,
        'static_errors': static_error,
        'test_results': yo,
        'question': obj,
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
    if request.method == "POST":
        request_dict = request.POST.dict()
        print(request_dict)
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

    time_started = TimeStarted.objects.all()
    questions = QuestionComposite.objects.all()
    sub_questions = SubQuestionComposite.object.all()
    submissions = Submission.object.all()
    static_lint = StaticLint.objects.all()
    results = Result.objects.all()
    sub_tests = Subtest.objects.all()

    lines.append(serialize(time_started))
 #   lines.append(serialize(questions))
 ##   lines.append(serialize(sub_questions))
 #   lines.append(serialize(submissions))
 #   lines.append(serialize(static_lint))
 #   lines.append(serialize(results))
 #   lines.append(serialize(sub_tests))

    response.writelines(lines)

    return response


def serialize(object):
    return serializers.serialize("yaml", object)
