from results.register_composite_test_decorator import RegisterCompositeTestClass
from results.setup_test_decorator import setup_test

from results.questions_test_case import QuestionsTestCase


@RegisterCompositeTestClass(question_number=1, question_part=3)
class TestQuestion3(QuestionsTestCase):

    @setup_test(max_mark=5)
    def test_point_1(self):
        from static_lint.code_to_lint import compute_score
        self.expectEqual(compute_score('Jessica ENNIS-HILL, 22.830, 12.540, 02:08.650'),
                         ('Jessica ENNIS-HILL', 1096, 1195, 984, 3275), msg='Jessica ENNIS-HILL, 22.830, 12.540, 02:08.650')

    @setup_test(max_mark=5)
    def test_point_2(self):
        from static_lint.code_to_lint import compute_score
        self.expectEqual(compute_score('Katarina JOHNSON-THOMPSON, 23.730, 13.480, 02:10.760'),
                         ('Katarina JOHNSON-THOMPSON', 1007, 1053, 954, 3014), msg='Katarina JOHNSON-THOMPSON, 23.730, 13.480, 02:10.760')

    @setup_test(max_mark=5)
    def test_point_3(self):
        from static_lint.code_to_lint import compute_score
        self.expectEqual(compute_score('Louise HAZEL, 24.480, 13.480, 02:18.780'),
                         ('Louise HAZEL', 935, 1053, 840, 2828), msg='Louise HAZEL, 24.480, 13.480, 02:18.780')


    @setup_test(max_mark=3)
    def test_zero_point(self):
        from static_lint.code_to_lint import compute_score
        self.expectEqual(compute_score('Liliane Blotty, 42.501, 27.480, 04:14.001'),
                         ('Liliane Blotty', 0, 0, 0, 0), msg='Liliane Blotty, 42.501, 27.480, 04:14.001')

    @setup_test(max_mark=1)
    def test_too_few_entries(self):
        from static_lint.code_to_lint import compute_score
        self.expectRaises(ValueError, compute_score, 'Liliane Blotty, 42.501, 27.480')

    @setup_test(max_mark=1)
    def test_too_many_entries(self):
        from static_lint.code_to_lint import compute_score
        self.expectRaises(ValueError, compute_score, 'Liliane Blotty, 42.501, 27.480, 04:14.001, 01:00.500')
