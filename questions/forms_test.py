import unittest
from django.test import TestCase
from questions.forms import QuestionForm


class QuestionFormTestCase(TestCase):
    def test_form_is_valid_when_given_answer(self):
        # Given
        form_data = {"answer": "model answer"}

        # When
        form = QuestionForm(data=form_data)

        # Then
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_when_answer_is_none(self):
        # Given
        form_data = {"answer": None}

        # When
        form = QuestionForm(data=form_data)

        # Then
        self.assertFalse(form.is_valid())

    def test_form_is_invalid_when_answer_is_empty(self):
        # Given
        form_data = {"answer": ""}

        # When
        form = QuestionForm(data=form_data)

        # Then
        self.assertFalse(form.is_valid())

    def test_form_(self):
        # Given
        form_data = {"answer": " "}

        # When
        form = QuestionForm(data=form_data)

        # Then
        self.assertFalse(form.is_valid())


if __name__ == '__main__':
    unittest.main()
