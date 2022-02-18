import unittest

from results.new_file import RegisterTestClass
from results.questions_test_case import QuestionsTestCase
from results.utils import setup_test


@RegisterTestClass(question_number=2)
class TestQuestion2(QuestionsTestCase):

    @setup_test(max_mark=2)
    def testSameSequences(self):
        from static_lint.code_to_lint import hammingDistance
        """ Test if a distance of 0 is returned when the sequences are 
        identical.
        """
        self.expectAlmostEqual(0, hammingDistance('lilian', 'lilian'), delta=0.000001, msg='lilian lilian')
        self.expectAlmostEqual(0, hammingDistance('1011001', '1011001'), delta=0.000001, msg='1011001 1011001')

    @setup_test(max_mark=2)
    def testCaseSensitive(self):
        from static_lint.code_to_lint import hammingDistance
        """ Test that the function is case sensitive. That is, the lower 
        case and upper case characters are considered different.
        """
        self.expectAlmostEqual(0, hammingDistance('Lilian', 'lilian'), delta=0.000001, msg='Lilian lilian')
        self.expectAlmostEqual(0, hammingDistance('Lilian', 'liLian'), delta=0.000001, msg='Lilian liLian')

    @setup_test(max_mark=2)
    def testGeneralCase(self):
        from static_lint.code_to_lint import hammingDistance
        """ Test that the function calculates the right distance for 
        different sequences.
        """
        self.expectAlmostEqual(3, hammingDistance('karolin', 'kathrin'), delta=0.000001, msg='karolin Kathrin')
        self.expectAlmostEqual(5, hammingDistance('10101', '01010'), delta=0.000001, msg='10101 01010')

    @setup_test(max_mark=2)
    def testInvalidSequencesLength(self):
        from static_lint.code_to_lint import hammingDistance
        """ Test that the function raise a ValueError if the sequences 
        provided are not comparable, that is do not have the same length.
        """
        self.expectRaises(ValueError, hammingDistance, 'caroline', 'catherine', msg='caroline catherine')
        self.expectRaises(ValueError, hammingDistance, 'catherine', 'caroline', msg='catherine caroline')


if __name__ == '__main__':
    unittest.main()
