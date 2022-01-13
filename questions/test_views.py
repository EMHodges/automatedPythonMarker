from django.test import TestCase

from questions.models import Question


class QuestionsViewsTestCase(TestCase):

    def setUp(self) -> None:
        self.question_1 = Question(number=1, description='description', answer='answer', mark=0,
                                   max_mark=10, method_name='method_name')
        self.question_2 = Question(number=2, description='description', answer='answer', mark=0,
                                   max_mark=10, method_name='method_name')
        self.question_1.save()
        self.question_2.save()

    def tearDown(self):
        """Depopulate created model instances from test database."""
        for obj in Question.objects.all():
            obj.delete()

    def test_question_list_view_displays_list_of_questions(self):
        # Given

        # When
        test_response = self.client.get('/questions/')

        # Then
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object_list' in test_response.context)
        self.assertEqual(len(test_response.context['object_list']), 2)
        self.assertTemplateUsed(test_response, 'question/question_list.html')
        self.assertEqual(test_response.context['object_list'][0], self.question_1)
        self.assertEqual(test_response.context['object_list'][1], self.question_2)


