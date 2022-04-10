from results.new_file import RegisterCompositeTestClass
from results.questions_test_case import QuestionsTestCase
from results.utils import setup_test

POINT_PARAMETERS = {"200m": (4.99087, 42.5, 1.81),
                    "800m": (0.11193, 254.0, 1.88),
                    "110m": (9.23076, 26.7, 1.835)}


@RegisterCompositeTestClass(question_number=1, question_part=2)
class TestQuestion2(QuestionsTestCase):

    @setup_test(max_mark=8)
    def test_points(self):
        from static_lint.code_to_lint import track_points
        self.expectEqual(track_points('13.480', POINT_PARAMETERS["110m"]), 1053, msg=f'13.480, {POINT_PARAMETERS["110m"]}')
        self.expectEqual(track_points('11.500', POINT_PARAMETERS["110m"]), 1361, msg=f'11.500, {POINT_PARAMETERS["110m"]}')
        self.expectEqual(track_points('23.000', POINT_PARAMETERS["200m"]), 1079, msg=f'23.000, {POINT_PARAMETERS["200m"]}')
        self.expectEqual(track_points('23.680', POINT_PARAMETERS["200m"]), 1012, msg=f'23.680, {POINT_PARAMETERS["200m"]}')
        self.expectEqual(track_points('02:40.550', POINT_PARAMETERS["800m"]), 567, msg=f'02:40.550, {POINT_PARAMETERS["800m"]}')
        self.expectEqual(track_points('02:11.310', POINT_PARAMETERS["800m"]), 946, msg=f'02:11.310, {POINT_PARAMETERS["800m"]}')

    @setup_test(max_mark=3)
    def test_zero_points(self):
        from static_lint.code_to_lint import track_points
        self.expectEqual(track_points('27.480', POINT_PARAMETERS["110m"]), 0, msg=f'27.480, {POINT_PARAMETERS["110m"]}')
        self.expectEqual(track_points('42.501', POINT_PARAMETERS["200m"]), 0, msg=f'42.501, {POINT_PARAMETERS["200m"]}')
        self.expectEqual(track_points('04:14.001', POINT_PARAMETERS["800m"]), 0, msg=f'04:14.001, {POINT_PARAMETERS["800m"]}')

    @setup_test(max_mark=1)
    def test_invalid_format_too_few_parameters(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '4:00.000', (0.11193, 254.0))

    @setup_test(max_mark=1)
    def test_invalid_format_too_many_parameters(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '4:00.000', (0.11193, 254.0, 1.267, 1.835))

    @setup_test(max_mark=0.5)
    def test_invalid_format_minutes(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '4:00.000', POINT_PARAMETERS["800m"])

    @setup_test(max_mark=0.5)
    def test_invalid_format_seconds(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '04:1.000', POINT_PARAMETERS["800m"])

    @setup_test(max_mark=0.5)
    def test_invalid_format_seconds2(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '01:61.000', POINT_PARAMETERS["800m"])

    @setup_test(max_mark=0.5)
    def test_invalid_format_fractionseconds(self):
        from static_lint.code_to_lint import track_points
        self.expectRaisess(ValueError, track_points, '04:01.5', POINT_PARAMETERS["800m"])
