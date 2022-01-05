import os
import re
from io import StringIO
from pathlib import Path

from pylint.reporters.text import TextReporter
from pylint.reporters.json_reporter import JSONReporter
from automatedPythonMarker.settings import resource_path
from static_lint.models import StaticLint
from pylint import lint
from pylint.reporters import text
from astroid import MANAGER

TMP_FILE = os.path.join('static_lint', 'code_to_lint.py')
LINT_RULES_FILE = os.path.join('static_lint', '.pylintrc')


def write_answer_to_tmp_file(answer):
    with open(TMP_FILE, 'w') as tmp_file:
        tmp_file.write(answer)
    with open(TMP_FILE, 'r') as tmp_file:
        print(tmp_file.read())


def lint_answer(answer, number):
    write_answer_to_tmp_file(answer)

    MANAGER.astroid_cache.clear()
    pylint_output = StringIO()  # need a StringIO object where the output will be stored
    args = [TMP_FILE, '--errors-only']
    lint.Run(args, reporter=JSONReporter(pylint_output), exit=False)  # exit=False means don't exit when the run is over
    StaticLint.objects.update_or_create(question_number=number, defaults={'feedback': pylint_output.getvalue()})


def format_lint_errors(lint_errors):
    pass


def format_lint_error(lint_error):
    pass


def format_lint_error_message(lint_message):
    pass
