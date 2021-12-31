from django.core.management.base import BaseCommand
import PyInstaller.__main__

import subprocess


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        subprocess.run(["python", "manage.py", "collectstatic", "--noinput"])
        PyInstaller.__main__.run([
            '--onefile',
            'automatedPythonMarker.spec',
            '-w',
        ])
