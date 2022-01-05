from django.apps import AppConfig


def setup_testRunner_for_questions():
    from .main import QUESTION_RUNNERS
    from .QuestionTestRunner import QuestionsTestRunner
    from questions.models import Question

    number_of_questions = Question.objects.values_list('number', flat=True)

    for question_number in number_of_questions:
        QUESTION_RUNNERS[question_number] = QuestionsTestRunner(question_number)


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'

    def ready(self):
        setup_testRunner_for_questions()