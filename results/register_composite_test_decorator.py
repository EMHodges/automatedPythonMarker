class RegisterCompositeTestClass:
    question_test_methods = {}

    def __init__(self, question_number, question_part, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._question_number = question_number
        self._question_part = question_part

    def __call__(self, cls):
        cls_test_methods = [method for method in dir(cls) if method.startswith('test')]
        test_methods = self.question_test_methods.get(self._question_number)
        if not test_methods:
            subquestion_test_methods = {self._question_part: cls_test_methods}
            self.question_test_methods[self._question_number] = subquestion_test_methods
        else:
            test_methods[self._question_part] = cls_test_methods
        return cls

    @staticmethod
    def get_test_question_number(test_name):
        for question_number, question_test_methods in RegisterCompositeTestClass.question_test_methods.items():
            for subquestion_part, subquestion_test_methods in question_test_methods.items():
                if test_name in subquestion_test_methods:
                    return question_number

    @staticmethod
    def get_test_question_part(test_name):
        for question_number, question_test_methods in RegisterCompositeTestClass.question_test_methods.items():
            for subquestion_part, subquestion_test_methods in question_test_methods.items():
                if test_name in subquestion_test_methods:
                    return subquestion_part
