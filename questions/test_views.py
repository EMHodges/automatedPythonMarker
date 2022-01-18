import responses
from django.test import TestCase
from django.urls import reverse

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

    def test_question_update_view(self):
        # Given
        url = reverse("questions:question-update", kwargs={'number': 1})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object' in test_response.context)
        self.assertTemplateUsed(test_response, 'question/question_update.html')
        self.assertEqual(test_response.context['object'], self.question_1)
        self.assertEqual(test_response.context['next_question'], self.question_2)
        self.assertEqual(test_response.context['previous_question'], None)
        self.assertEqual(test_response.context['static_errors'], None)
        self.assertQuerysetEqual(test_response.context['test_results'], [])

    def test_question_update_view_shows_404_if_question_not_found(self):
        # Given
        url = reverse("questions:question-update", kwargs={'number': 100})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 404)

    def test_question_update_view_next_question(self):
        url = reverse("questions:question-update", kwargs={'number': 1})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['next_question'], self.question_2)

    def test_question_update_view_next_question_None(self):
        url = reverse("questions:question-update", kwargs={'number': 2})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['next_question'], None)

    def test_question_update_view_next_question_skips(self):
        question_4 = Question(number=4, description='description', answer='answer', mark=0,
                              max_mark=10, method_name='method_name')
        question_4.save()

        url = reverse("questions:question-update", kwargs={'number': 2})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['next_question'], question_4)

    def test_question_update_view_previous_question(self):
        url = reverse("questions:question-update", kwargs={'number': 2})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['previous_question'], self.question_1)

    def test_question_update_view_previous_question_None(self):
        url = reverse("questions:question-update", kwargs={'number': 1})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['previous_question'], None)

    def test_question_update_view_previous_question_skips(self):
        question_4 = Question(number=4, description='description', answer='answer', mark=0,
                              max_mark=10, method_name='method_name')
        question_4.pk = 4
        question_4.save()

        url = reverse("questions:question-update", kwargs={'number': 4})

        test_response = self.client.get(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertEqual(test_response.context['previous_question'], self.question_2)

    @responses.activate
    def test_question_update_view_previous_question_post(self):
        url = reverse("questions:question-update", kwargs={'number': 1})

        responses.add(responses.POST, url, json={"answer": 'yo'}, status=200)

        q = Question(number=1, description='d', answer='a', mark=0, max_mark=0, method_name='m')

        test_response = self.client.post(url)

        self.assertEqual(test_response.status_code, 200)
        self.assertTrue(False)
        self.assertEqual(test_response.context['previous_question'], None)

    def test_question_list_view_displays_list_of_questions(self):
        # Given
        url = reverse("questions:question-list")

        # When
        test_response = self.client.get(url)

        # Then
        self.assertEqual(test_response.status_code, 200)
        self.assertTrue('object_list' in test_response.context)
        self.assertEqual(len(test_response.context['object_list']), 2)
        self.assertTemplateUsed(test_response, 'question/question_list.html')
        self.assertEqual(test_response.context['object_list'][0], self.question_1)
        self.assertEqual(test_response.context['object_list'][1], self.question_2)


