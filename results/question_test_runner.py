import unittest

from questions.models import SubQuestionComposite, QuestionComposite
from submission.models import Submission
from .questions_text_test_result import QuestionsTextTestResult


class QuestionsTestRunner(unittest.TextTestRunner):
    '''
    classdocs
    '''
    def __init__(self, question_number, question_part):
        self.question_number = question_number
        self.question_part = question_part
        super(QuestionsTestRunner, self).__init__()

    def _makeResult(self):
        question = QuestionComposite.objects.get(number=self.question_number)
        sub_question = SubQuestionComposite.object.get(question=question, part=self.question_part)
        submission_number = Submission.object.get_next_submission_number(sub_question)
        submission = Submission.object.create(sub_question=sub_question, submission_number=submission_number)
        submission.save()
        print('making result')
        return QuestionsTextTestResult(self.question_number, self.question_part, submission, self.stream, self.descriptions, self.verbosity)
