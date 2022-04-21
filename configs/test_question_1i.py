from results.register_composite_test_decorator import RegisterCompositeTestClass
from results.questions_test_case import QuestionsTestCase
from results.setup_test_decorator import setup_test


@RegisterCompositeTestClass(question_number=1, question_part=1)
class TestQuestion1(QuestionsTestCase):

    @setup_test(max_mark=7)
    def test_minutes_seconds(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectAlmostEqual(time_to_seconds('04:00.000'), 240.0, msg='04:00.000')
        self.expectAlmostEqual(time_to_seconds('02:15.000'), 135.0, msg='02:15.000')
        self.expectAlmostEqual(time_to_seconds('02:05.520'), 125.52, msg='02:05.520')
        self.expectAlmostEqual(time_to_seconds('01:59.999'), 119.999, msg='01:59.999')

    @setup_test(max_mark=4)
    def test_seconds_only(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectAlmostEqual(time_to_seconds('10.530'), 10.53, msg='10.530')

    @setup_test(max_mark=1)
    def test_invalid_minutes_format(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectRaises(ValueError, time_to_seconds, '4:00.000')

    @setup_test(max_mark=1)
    def test_invalid_seconds_format(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectRaises(ValueError, time_to_seconds, '04:1.000')

    @setup_test(max_mark=1)
    def test_invalid_seconds2_format(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectRaises(ValueError, time_to_seconds, '01:61.000')

    @setup_test(max_mark=1)
    def test_invalid_fractionseconds_format(self):
        from static_lint.code_to_lint import time_to_seconds
        self.expectRaises(ValueError, time_to_seconds, '04:01.5')
