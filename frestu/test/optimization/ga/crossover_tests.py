import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.crossover import *


class CrossoverTests(unittest.TestCase):

    def setUp(self):
        self.vec_1 = np.array([1, 2, 3, 4, 5])
        self.vec_2 = np.array([6, 7, 8, 9, 0])
    
    def tearDown(self):
        pass

    def test_crossover_n_point(self):
        vec = crossover_n_point(self.vec_1, self.vec_2, n_point=1)
        # HACK: 
        # 遺伝子が交換されていることをテストし、交換のされ方はテストできていない。
        self.assertEqual(list(vec == self.vec_1), list(vec != self.vec_2))
        self.assertEqual(list(vec == self.vec_2), list(vec != self.vec_1))

    def test_crossover_uniform(self):
        vec = crossover_uniform(self.vec_1, self.vec_2)
        # HACK: 
        # 遺伝子が交換されていることをテストし、交換のされ方はテストできていない。
        self.assertEqual(list(vec == self.vec_1), list(vec != self.vec_2))
        self.assertEqual(list(vec == self.vec_2), list(vec != self.vec_1))


if __name__ == '__main__':
    unittest.main()