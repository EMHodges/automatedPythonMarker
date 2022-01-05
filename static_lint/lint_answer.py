import json
import os
import re
from io import StringIO

from pylint.reporters.json_reporter import JSONReporter
from static_lint.models import StaticLint
from pylint import lint
from astroid import MANAGER

TMP_FILE = os.path.join('static_lint', 'code_to_lint.py')
LINT_RULES_FILE = os.path.join('static_lint', '.pylintrc')


def lint_answer(answer, number):
    write_answer_to_tmp_file(answer)
    lint_errors = get_lint_errors()
    formatted_lint_errors = format_lint_errors(lint_errors)
    StaticLint.objects.update_or_create(question_number=number, defaults={'feedback': formatted_lint_errors})


def write_answer_to_tmp_file(answer):
    with open(TMP_FILE, 'w') as tmp_file:
        tmp_file.write(answer)


def get_lint_errors():
    clear_pylint_cache()
    pylint_output = StringIO()
    args = [TMP_FILE, '--errors-only']
    lint.Run(args, reporter=JSONReporter(pylint_output), exit=False)
    return pylint_output.getvalue()


def clear_pylint_cache():
    MANAGER.astroid_cache.clear()


def format_lint_errors(lint_errors):
    lint_errors = json.loads(lint_errors)
    formatted_lint_errors = [format_lint_error(lint_error) for lint_error in lint_errors]
    return ''.join(formatted_lint_errors)


def format_lint_error(lint_error):
    formatted_error_message = format_lint_error_message(lint_error['message'])
    return f"line {lint_error['line']}, column {lint_error['column']}: {formatted_error_message}"


def format_lint_error_message(message):
    unknown_line = re.compile(r"\(<unknown>, line \d*\)")
    return unknown_line.sub('', message)
