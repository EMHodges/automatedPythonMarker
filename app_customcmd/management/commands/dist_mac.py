from django.core.management.base import BaseCommand
import PyInstaller.__main__

from questions.models import SubQuestionComposite
from results.models import Result, Subtest
from static_lint.models import StaticLint
import shutil


# ToDo make this and dist_win one command and add command options e.g. python manage.py dist mac or python manage.py dist win
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self._clear_databases()
        self._remove_generated_files()

        PyInstaller.__main__.run([
            'automatedPythonMarker.spec',
            '-w',  # Creates a .app executable
            '--onefile',
            '--clean'
        ])

    @staticmethod
    def _clear_databases():
        StaticLint.objects.all().delete()
        Subtest.objects.all().delete()
        Result.objects.all().delete()
        SubQuestionComposite.objects.all().update(answer=None)

    @staticmethod
    def _remove_generated_files():
        shutil.rmtree('build/', ignore_errors=True)
        shutil.rmtree('dist/', ignore_errors=True)
        shutil.rmtree('static_lint/code_to_lint.py', ignore_errors=True)
