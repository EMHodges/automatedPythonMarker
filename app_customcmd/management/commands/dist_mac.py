from django.core.management.base import BaseCommand
import PyInstaller.__main__

from static_lint.models import StaticLint


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        StaticLint.objects.all().delete()

        PyInstaller.__main__.run([
            'automatedPythonMarker.spec',
            '-w', # Creates a .app executable
            '--onefile'
        ])
