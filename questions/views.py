import re
import sys

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from submission.models import Submission, TimeStarted
from submission.forms import SubmissionForm
from .models import QuestionComposite, SubQuestionComposite
from results.main import run_tests, create_submission
from results.models import Result, Subtest
from django.core import serializers


# Create your views here.
def question_update_view(request, number):
    obj = get_object_or_404(QuestionComposite, number=number)
    sub_objs = obj.subquestioncomposite_set.all()

    timestamp_first_submission()

    fords = {}

    yo = {}
    static_error = {}

    if request.method == "POST":
        request_dict = request.POST.dict()
        for key, value in request_dict.items():
            answer_key = re.match(r'\d+-answer', key)
            if answer_key:
                first_letter = int(key[0])

                for sub_obj in sub_objs:
                    if first_letter == sub_obj.part:
                        submission = create_submission(number, first_letter)
                        form = SubmissionForm(request.POST or None, instance=submission, prefix=str(first_letter))
                        form_answer = request.POST.get(key)
                        if form.is_valid():
                            form.save()
                            x = get_object_or_404(QuestionComposite, number=number).subquestioncomposite_set.get(
                                part=first_letter)
                            fords[x] = form
                            run_tests(form_answer, number, first_letter, submission)
                    else:
                        submission = Submission.object.get_last_submission(sub_obj)
                        fords[sub_obj] = SubmissionForm(None, instance=submission, prefix=int(sub_obj.part))
    else:
        for objz in sub_objs:
            submission = Submission.object.get_last_submission(objz)
            fords[objz] = SubmissionForm(None, instance=submission, prefix=int(objz.part))

    for objz in sub_objs:
        last_submission = Submission.object.get_last_submission(objz)
        if (hasattr(last_submission, 'staticlint')):
            static_error[objz] = last_submission.staticlint
        else:
            static_error[objz] = None
        yo[objz] = Result.objects.filter(question_number=number, question_part=objz.part, submission=last_submission)
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


def timestamp_first_submission():
    time_obj = TimeStarted.objects.get_or_none()
    if not time_obj:
        time = TimeStarted()
        time.save()


def question_list_view(request):
    queryset = QuestionComposite.objects.all()
    context = {
        "object_list": queryset
    }
    return render(request, "question/question_list.html", context)


def question_generate_submission_file_view(request):
    filename = generate_filename()

    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}.txt'

    objects_to_save = [
        TimeStarted.objects.all(),
        QuestionComposite.objects.all(),
        SubQuestionComposite.object.all(),
        Submission.object.all(),
        StaticLint.objects.all(),
        Result.objects.all(),
        Subtest.objects.all()
    ]

    lines = [serialize(objects) for objects in objects_to_save]
    response.writelines(lines)
    return response


def generate_filename():
    pattern = re.compile(r'(python-marker\d{6})')

    filename = 'python-marker'
    for arg in sys.argv:
        match = pattern.search(arg)
        if match:
            filename = match.group(1)
    return filename


def serialize(object):
    return serializers.serialize("yaml", object)
