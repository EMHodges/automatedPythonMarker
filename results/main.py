import importlib
import unittest
from functools import wraps

from automatedPythonMarker.settings import resource_path

from .QuestionTestRunner import QuestionsTestRunner


def run_tests_for_file(module_name, file_name='results/test_question_1.py'):
    question_runner = QuestionsTestRunner(1)
    print('in run tests for file')
    spec = importlib.util.spec_from_file_location('yo', file_name)
    print(spec)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ImportError:
        print('not implemented')
    print(module)
    suite = unittest.TestLoader().loadTestsFromModule(module)
    print(suite)
    x = run_suite(question_runner, suite)
    print(x)




def run_suite(question_runner, suite):
    question_runner.run(suite)



if __name__ == "__main__":
    run_tests_for_file('yo', 'test_question_1.py')
