import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.crossover import *


class CrossoverTests(unittest.TestCase):

    def setUp(self):
        self.vec1 = np.array([1, 2, 3, 4, 5])
        self.vec2 = np.array([6, 7, 8, 9, 0])
    
    def tearDown(self):
        pass

    def test_crossover_n_point(self):
        vec = crossover_n_point(self.vec1, self.vec2, n_point=1)
        # HACK: 
        # 遺伝子が交換されていることをテストし、交換のされ方はテストできていない。
        self.assertEqual(list(vec == self.vec1), list(vec != self.vec2))
        self.assertEqual(list(vec == self.vec2), list(vec != self.vec1))


if __name__ == '__main__':
    unittest.main()