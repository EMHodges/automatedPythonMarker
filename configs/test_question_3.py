import importlib
import os
import unittest

from automatedPythonMarker.settings import resource_path
from results.questions_test_case import QuestionsTestCase
from results.utils import setup_test


class TestQuestion3(QuestionsTestCase):

    def setUp(self) -> None:
        import static_lint.code_to_lint
        importlib.reload(static_lint.code_to_lint)


    def sameIndices(self, expected, actual):
        print('in same indices')
        print(actual)
        """ This is a convenience function to compare the two dictionaries passed
        in parameters. It is needed to ensure that the word passed as keys of
        the dictionary are not case sensitive.

        For example, given:
        expected = {'One': [2,7]} and actual = {'one':[2, 7]} the function call
        sameIndices(expected, actual) would return True.

        On the other hand, given:
        expected = {'One': [2]} and actual = {'one':[3]} the function call
        sameIndices(expected, actual) would raise an AssertionError meaning
        the test has failed.
        """
        self.assertEqual(len(expected), len(actual))
        for word in actual:
            self.assertListEqual(expected[word.lower()], actual[word])

        return True

    @setup_test(max_mark=2)
    def testSingleWord(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that given an input containing only one word, the correct
        result is returned.
        """
        c = resource_path(os.path.join("configs", "data", "oneWord.txt"))
        self.assertTrue(self.sameIndices({'one': [0]},
                                         getWordsIndices(c)))

    @setup_test(max_mark=2)
    def testNonExistingFile(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that the function returns None if the file does not exist or
        there is an exception whilst reading the file.
        """
        self.assertIsNone(getWordsIndices('doesNotExist.txt'))

    @setup_test(max_mark=2)
    def testSingleWordStartWithSpace(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that given an input containing only one word and starting with
        a blank space, the correct result is returned. Watch out for the shift
        in the indices.
        """
        self.assertTrue(self.sameIndices({'one': [1]},
                                         getWordsIndices('data//oneSpaceAndOneWord.txt')))

    @setup_test(max_mark=3)
    def testTwoWordsSingleSpace(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that the correct output is returned when there is no duplicate
        words and a single blank space between words.
        """
        self.assertTrue(self.sameIndices({'one': [0], 'two': [4]},
                                         getWordsIndices('data//twoWords.txt')))

    @setup_test(max_mark=3)
    def testTwoWordsMultipleSpace(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that the correct output is returned when there is no duplicate
        words and multiple blank spaces between words.
        """
        self.assertTrue(self.sameIndices({'one': [0], 'two': [6]},
                                         getWordsIndices('data//twoWordsTwoSpaces.txt')))

    @setup_test(max_mark=8)
    def testMultipleWordsMultipleIndicies(self):
        from static_lint.code_to_lint import getWordsIndices
        """ Test that the correct output is returned when there are duplicate 
        words and multiple indices for the same word. Note that the function 
        should be case incensitive, for example 'One' and 'one' are considered
        to be the same word.
        """
        self.assertTrue(self.sameIndices({'one': [0, 14], 'two': [4], 'three': [8, 19]},
                                         getWordsIndices('data//multipleWords.txt')))


if __name__ == '__main__':
    unittest.main()

