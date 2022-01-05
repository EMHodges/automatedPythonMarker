from django.core.management.base import BaseCommand
import PyInstaller.__main__

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        PyInstaller.__main__.run([
            'automatedPythonMarker.spec',
            '--onefile'
        ])