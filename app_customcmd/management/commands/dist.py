from django.core.management.base import BaseCommand
import PyInstaller.__main__
import shutil

from app_customcmd.management.functions.delete_from_databases import delete_answers
from configs.constants import TMP_FILE


def run_windows():
    PyInstaller.__main__.run([
        'automatedPythonMarker.spec',
        '--onefile'
    ])


def run_mac():
    PyInstaller.__main__.run([
        'python-marker.spec',
        '-w',  # Creates a .app executable
        '--onefile',
        '--clean'
    ])


os_args = {
    "w": run_windows,
    "m": run_mac,
    "win": run_windows,
    "mac": run_mac,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('os', nargs="+", type=str)

    def handle(self, *args, **kwargs):
        delete_answers()
        self._remove_generated_files()

        os = kwargs['os'][0]
        try:
            os_args[os]()
        except Exception as e:
            print("Unable to create executable")
            print(e)

    @staticmethod
    def _remove_generated_files():
        shutil.rmtree('build/', ignore_errors=True)
        shutil.rmtree('dist/', ignore_errors=True)
        shutil.rmtree(TMP_FILE, ignore_errors=True)
