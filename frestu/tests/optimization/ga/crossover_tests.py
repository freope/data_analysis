import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.crossover import *


class CrossoverTests(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_crossover_n_point(self):
        crossover_n_point()


if __name__ == '__main__':
    unittest.main()