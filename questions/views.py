import re

from django.shortcuts import render, get_object_or_404

from static_lint.models import StaticLint
from submission.models import Submission
from .forms import QuestionForm
from .models import Question, QuestionComposite, SubQuestionComposite
from results.main import run_testing
from results.models import Result, Subtest


# Create your views here.
def question_update_views(request, number):
    obj = get_object_or_404(QuestionComposite, number=number)

    sub_objs = obj.subquestioncomposite_set.all()

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
                        sub_question = SubQuestionComposite.object.get(part=first_letter)
                        form = QuestionForm(request.POST or None, instance=sub_question, prefix=str(first_letter))
                        form_answer = request.POST.get(key)

                        if form.is_valid():
                            form.save()
                            x = get_object_or_404(QuestionComposite, number=number).subquestioncomposite_set.get(
                                part=first_letter)
                            fords[x] = form
                            run_testing(form_answer, number, first_letter)
                            # static_errors = StaticLint.objects.get(question_number=number)
                    else:
                        fords[sub_obj] = QuestionForm(None, instance=sub_obj, prefix=int(sub_obj.part))
    else:
        for objz in sub_objs:
            fords[objz] = QuestionForm(None, instance=objz, prefix=int(objz.part))

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
