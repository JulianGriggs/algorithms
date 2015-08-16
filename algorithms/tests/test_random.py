import unittest
from ..random import mersenne_twister, minimum_edit_distance as med


class TestMersenneTwister(unittest.TestCase):
    """
    Tests Mersenne Twister values for several seeds comparing against
    expected values from C++ STL's Mersenne Twister implementation
    """
    
    def test_mersenne_twister(self):
        mt = mersenne_twister.MersenneTwister()

        #Test seed 1
        mt.seed(1)
        self.expected = [1791095845, 4282876139, 3093770124,
                         4005303368, 491263, 550290313, 1298508491,
                         4290846341, 630311759, 1013994432]
        self.results = []
        for i in range(10):
            self.results.append(mt.randint())
        self.assertEqual(self.expected, self.results)

        #Test seed 42
        mt.seed(42)
        self.expected = [1608637542, 3421126067, 4083286876,
                         787846414, 3143890026, 3348747335,
                         2571218620, 2563451924, 670094950, 1914837113]
        self.results = []
        for i in range(10):
            self.results.append(mt.randint())
        self.assertEqual(self.expected, self.results)

        #Test seed 2147483647
        mt.seed(2147483647)
        self.expected = [1689602031, 3831148394, 2820341149,
                         2744746572, 370616153, 3004629480,
                         4141996784, 3942456616, 2667712047, 1179284407]
        self.results = []
        for i in range(10):
            self.results.append(mt.randint())
        self.assertEqual(self.expected, self.results)

        #Test seed -1
        #Hex is used to force 32-bit -1
        mt.seed(0xffffffff)
        self.expected = [419326371, 479346978, 3918654476,
                         2416749639, 3388880820, 2260532800,
                         3350089942, 3309765114, 77050329, 1217888032]
        self.results = []
        for i in range(10):
            self.results.append(mt.randint())
        self.assertEqual(self.expected, self.results)


class TestMinimumEditDistance(unittest.TestCase):
    '''
    Tests finding the minimum edit distance between two strings.
    '''
    def apply(self, test_cases):
        for test in test_cases:
            self.assertEqual(med.min_edit_distance(test[0], test[1]), test[2])


    def test_empty_strings(self):
        test_cases = [("", "", 0),
                      ("a", "", 1),
                      ("", "a", 1),
                      ("abc", "", 3),
                      ("", "abc", 3)]
        self.apply(test_cases)

    def test_equal_strings(self):
        test_cases = [("", "", 0),
                      ("a", "a", 0),
                      ("abc", "abc", 0)]
        self.apply(test_cases)

    def test_when_only_inserts_are_needed(self):
        test_cases = [("", "a", 1),
                      ("a", "ab", 1),
                      ("b", "ab", 1),
                      ("ac", "abc", 1),
                      ("abcdefg", "xabxcdxxefxgx", 6)]
        self.apply(test_cases)
 
    def test_when_only_deletes_are_needed(self):
        test_cases = [("a", "", 1),
                      ("ab", "a", 1),
                      ("ab", "b", 1),
                      ("abc", "ac", 1),
                      ("xabxcdxxefxgx", "abcdefg", 6)]
        self.apply(test_cases)

    def test_when_only_substitutions_are_needed(self):
        test_cases = [("a", "b", 2),
                      ("ab", "ac", 2),
                      ("ac", "ab", 2),
                      ("abc", "axc", 2),
                      ("xabxcdxxefxgx", "1ab2cd34ef5g6", 12)]
        self.apply(test_cases)
 
    def test_when_many_operations_are_needed(self):
        test_cases = [("intention", "execution", 8),
                      ("intention", "executio", 9),
                      ("intention", "xecutio", 8)]

        self.apply(test_cases)
