class RegisterTestClass:
    test_method_names_for_question = {}

    def __init__(self, question_number, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._question_number = question_number

    def __call__(self, cls):
        test_methods = [method for method in dir(cls) if method.startswith('test')]
        self.test_method_names_for_question[self._question_number] = test_methods
        return cls

    @staticmethod
    def get_test_question_number(test_name):
        for key, value in RegisterTestClass.test_method_names_for_question.items():
            if test_name in value:
                return key