from questions.models import SubQuestionComposite, QuestionComposite
from results.models import Result, Subtest
from static_lint.models import StaticLint
from submission.models import Submission, TimeStarted


def delete_databases_content():
    Subtest.objects.all().delete()
    Result.objects.all().delete()
    StaticLint.objects.all().delete()
    Submission.objects.all().delete()
    SubQuestionComposite.object.all().delete()
    QuestionComposite.objects.all().delete()
    TimeStarted.objects.all().delete()


def delete_answers():
    Subtest.objects.all().delete()
    Result.objects.all().delete()
    StaticLint.objects.all().delete()
    Submission.objects.all().delete()
    TimeStarted.objects.all().delete()