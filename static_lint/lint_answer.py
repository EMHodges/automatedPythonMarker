import os
import re
from io import StringIO
from automatedPythonMarker.settings import resource_path
from static_lint.models import StaticLint
from pylint import lint
from pylint.reporters import text

TMP_FILE = os.path.join('static_lint', 'code_to_lint.py')
LINT_RULES_FILE = os.path.join('static_lint', '../questions/.pylintrc')


def write_answer_to_tmp_file(answer):
    with open('code_to_lint.py', 'w') as tmp_file:
        tmp_file.write(answer)
    with open('code_to_lint.py', 'r') as tmp_file:
        print(tmp_file.read())

def lint_answer(answer, number):
    write_answer_to_tmp_file(answer)

    pylint_output = StringIO()  # need a StringIO object where the output will be stored
    reporter = text.ColorizedTextReporter(pylint_output)
    args = [TMP_FILE, f"--rcfile='{'questions/.pylintrc'}'"]
    run = lint.Run(args, reporter=reporter, exit=False)  # exit=False means don't exit when the run is over
    print(run)
    print(pylint_output.getvalue())
   # (pylint_stdout, pylint_stderr) = lint.py_run("code_to_lint.py", return_std=True)

   # print(lint.py_run)
   # print(pylint_stdout.getvalue())
   # print('error')
   # print(pylint_stderr.getvalue())
   # print('end error')
   # print(type(pylint_stdout.getvalue()))
   # modified_outputs = pylint_stdout.getvalue().split("\n", 1)[1]
   # unknown_line = re.compile(r"\(<unknown>, line \d*\)")
   # modified_outputs = unknown_line.sub('', modified_outputs)
   # print(modified_outputs, end="")

    StaticLint.objects.update_or_create(question_number=number, defaults={'feedback': pylint_output.getvalue()})


def format_lint_errors(lint_errors):
    pass


def format_lint_error(lint_error):
    pass


def format_lint_error_message(lint_message):
    pass
