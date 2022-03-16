import unittest

from results.new_file import RegisterTestClass, RegisterCompositeTestClass

from results.questions_test_case import QuestionsTestCase
from results.utils import setup_test


@RegisterCompositeTestClass(question_number=4, question_part=2)
class TestQuestion4ii(QuestionsTestCase):

    @setup_test(max_mark=2)
    def testSameSequences(self):
        from static_lint.code_to_lint import yop
        """ Test if a distance of 0 is returned when the sequences are 
        identical.
        """
        self.expectAlmostEqual(0, yop(0,0,0), delta=0.000001, msg='lilian lilian')

    @setup_test(max_mark=2)
    def testCaseSensitive(self):
        from static_lint.code_to_lint import yop
        """ Test if a distance of 0 is returned when the sequences are 
        identical.
        """
        self.expectAlmostEqual(3, yop(1,0,0), delta=0.000001, msg='lilian lilian')

    @setup_test(max_mark=2)
    def testGeneralCase(self):
        from static_lint.code_to_lint import yop
        """ Test if a distance of 0 is returned when the sequences are 
        identical.
        """
        self.expectAlmostEqual(0, yop(0,0,0), delta=0.000001, msg='lilian lilian')

    @setup_test(max_mark=2)
    def testInvalidSequencesLength(self):
        from static_lint.code_to_lint import yop
        """ Test if a distance of 0 is returned when the sequences are 
        identical.
        """
        self.expectAlmostEqual(6, yop(2,0,0), delta=0.000001, msg='lilian lilian')

if __name__ == '__main__':
    unittest.main()
