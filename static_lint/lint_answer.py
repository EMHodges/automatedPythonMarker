from static_lint.models import StaticLint


def lint_answer(answer, number):
    StaticLint.objects.update_or_create(question_number=number, defaults={'feedback': answer})