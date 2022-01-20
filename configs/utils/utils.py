import os.path

from automatedPythonMarker.settings import resource_path
import re


def absolute_test_data_path(relative_test_data_path):
    x = re.split('//|/|\\\\', relative_test_data_path)
    relative_path = os.path.join("configs", *x)
    absolute_path = resource_path(relative_path)
    return absolute_path
