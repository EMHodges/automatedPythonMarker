import json
import os
import re
import shutil
from io import StringIO
from automatedPythonMarker.settings import resource_path
from pylint.reporters.json_reporter import JSONReporter

from static_lint.models import StaticLint
from pylint import lint
from astroid import MANAGER

TMP_FILE = resource_path(os.path.join('static_lint', 'code_to_lint.py'))
LINT_RULES_FILE = os.path.join('static_lint', '.pylintrc')


def lint_answer(answer, number):
    write_answer_to_tmp_file(answer)
    lint_errors = get_lint_errors()
    formatted_lint_errors = format_lint_errors(lint_errors)
    StaticLint.objects.update_or_create(question_number=number, defaults={'feedback': formatted_lint_errors})


def linting_answer(number, submission, question_part):
    lint_errors = get_lint_errors()
    formatted_lint_errors = format_lint_errors(lint_errors, question_part)
    static_lint = StaticLint(question_number=number, submission=submission, feedback=formatted_lint_errors)
    static_lint.save()


def write_answer_to_tmp_file(answer):
    shutil.rmtree(TMP_FILE, ignore_errors=True)
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


def format_lint_errors(lint_errors, question_part):
    lint_errors = json.loads(lint_errors)
    formatted_lint_errors = [format_lint_error(lint_error, question_part) for lint_error in lint_errors]
    return ''.join(formatted_lint_errors)


def format_lint_error(lint_error, question_part):
    formatted_error_message = format_lint_error_message(lint_error['message'])
    line_number = get_line_number(lint_error['line'], question_part)
    return f"line {line_number}, column {lint_error['column']}: {formatted_error_message}"


def get_line_number(line_number, question_part):
    if question_part == 2:
        return line_number - 27
    elif question_part == 3:
        return line_number - 37
    return line_number


def format_lint_error_message(message):
    unknown_line = re.compile(r"\(<unknown>, line \d*\)")
    message = unknown_line.sub('', message)
    if message == 'unindent does not match any outer indentation level ':
        return 'Indentation Error - ensure code is indented correctly'
    return message
