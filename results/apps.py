import os.path

from django.apps import AppConfig

QUESTION_TEST_FILES = {}
QUESTION_RUNNERS = {}


class ResultsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'

    def ready(self):
        self._setup_testRunner_for_questions()

    def _setup_testRunner_for_questions(self):
        from .question_test_runner import QuestionsTestRunner
        from questions.models import Question

        number_of_questions = Question.objects.values_list('number', flat=True)

        for question_number in number_of_questions:
            QUESTION_RUNNERS[question_number] = QuestionsTestRunner(question_number)
            self._add_test_file_paths(question_number)

    def _add_test_file_paths(self, question_number):
        from automatedPythonMarker.settings import resource_path

        file_path = resource_path(os.path.join("configs", f"test_question_{str(question_number)}.py"))
        is_valid_file_path = os.path.isfile(file_path)

        if not is_valid_file_path:
            QUESTION_TEST_FILES.clear()
            raise FileNotFoundError(f"The test file for question: {question_number} cannot be found - looked for: "
                                    f"{file_path}. The test file should be called: 'test_question_{question_number}")
        QUESTION_TEST_FILES[question_number] = file_path
