import os

from automatedPythonMarker.settings import resource_path

TMP_FILE = resource_path(os.path.join('static_lint', 'code_to_lint.py'))
LINT_RULES_FILE = os.path.join('static_lint', '.pylintrc')

