import ast
import functools

from automatedPythonMarker.settings import resource_path
from questions.models import Question
from results.questions_test_case import QuestionsTestCase
from results.apps import QUESTION_TEST_FILES
from static_lint.models import StaticLint
import re


class my_deco:
    all_results = {}

    def __init__(self, gp=None, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.gp = gp

    def __call__(self, cls):
        method_list = [method for method in dir(cls) if method.startswith('test')]
        self.all_results[self.gp] = method_list
        return cls


def class_registers(cls):
    print(cls)
    for name in dir(cls):
        method = getattr(cls, )
        method

    method_list = [method for method in dir(cls) if method.startswith('test')]
    cls._yo = method_list
    return cls


# Could either add method list to question itself, or define a
# dict on class_register and access it that way - maybe better other way may need funny db

def class_register(no):
    def yo(cls):
        print('call')
        method_list = [method for method in dir(cls) if method.startswith('test')]
        class_register.dic[no] = method_list
        print(class_register.dic)
        return cls

    return yo


class_register.dic = {}


def class_registerss(cls):
    method_list = [method for method in dir(cls) if method.startswith('test')]
    class_register._yo = method_list
    return cls


def makeRegistrar(cls):
    registry = {}

    def registrar(clss):
        method_list = [method for method in dir(clss) if method.startswith('test')]
        registry[clss.__name__] = method_list
        return clss  # normally a decorator returns a wrapped function,
        # but here we return func unmodified, after registering it

    registrar.all = registry
    return registrar


def register(*args):
    def wrapper(func):
        func._prop = args
        return func

    return wrapper


def register_test_cases():
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            print('in reg')
            print(func)

        return decorated

    return decorator


def setup_test(max_mark):
    def decorator(func):
        @functools.wraps(func)
        def decorated(*args, **kwargs):
            test_case_instance: QuestionsTestCase = args[0]

            check_import_error(test_case_instance)

            func(*args, **kwargs)
            test_case_instance.set_mark(max_mark)

        return decorated

    return decorator


def extract_method_names():
    source = open(resource_path('static_lint/code_to_lint.py')).read()
    return [node.name for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]


def check_import_error(test_case: QuestionsTestCase) -> None:
    module_method_names = extract_method_names()
    question_number = test_case.get_question_number()
    method_under_test = Question.objects.get(number=question_number).method_name
    if method_under_test not in module_method_names:
        test_case.fail("@Import error")


def check_syntax_error(test_case: QuestionsTestCase) -> None:
    test_case_class_name = test_case.__class__.__name__
    test_case_question_number = re.split('TestQuestion', test_case_class_name)[-1]

    syntax_errors_for_question = StaticLint.objects.get(question_number=int(test_case_question_number))

    if syntax_errors_for_question.feedback:
        test_case.fail("@Syntax error")


def extract_test_names(question_number):
    source = open(QUESTION_TEST_FILES[question_number]).read()

    for node in ast.parse(source).body:
        if isinstance(node, ast.ClassDef) and node.name == f'TestQuestion{question_number}':
            return [function.name for function in node.body if
                    isinstance(function, ast.FunctionDef) and function.name.startswith("test")]
