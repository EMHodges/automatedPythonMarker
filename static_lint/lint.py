import json
import os.path
import re

from pylint import epylint as lint

from .models import StaticLint

TMP_FILE = os.path.join('static_lint', 'code_to_lint.py')
LINT_RULES_FILE = os.path.join('static_lint', '../questions/.pylintrc')


def lint_answer(answer: str, question_number: int) -> None:
    write_answer_to_tmp_file(answer)

    (pylint_stdout, pylint_stderr) = lint.py_run(f"{TMP_FILE} --rcfile='{LINT_RULES_FILE}'", return_std=True)

    formatted_lint_errors = format_lint_errors(pylint_stdout.getvalue())

    StaticLint.objects.update_or_create(question_number=question_number,
                                        defaults={'feedback': formatted_lint_errors})


def write_answer_to_tmp_file(answer):
    with open(TMP_FILE, "w") as tmp_file:
        tmp_file.write(answer)


def format_lint_errors(lint_errors: str) -> str:
    lint_errors = json.loads(lint_errors)
    formatted_lint_errors = [format_lint_error(lint_error) for lint_error in lint_errors]
    return ''.join(formatted_lint_errors)


def format_lint_error(error):
    formatted_error_message = format_lint_error_message(error['message'])
    return f"line {error['line']}, column {error['column']}: {formatted_error_message}"


def format_lint_error_message(message):
    unknown_line = re.compile(r"\(<unknown>, line \d*\)")
    return unknown_line.sub('', message)
