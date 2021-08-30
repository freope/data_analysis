import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga import Individual
from frestu.optimization.ga import Population
from frestu.optimization.ga.crossover import *


class PopulationTests(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_alternate(self):
        pass

    def test_create(self):
        print('---- ABC')
        pass        


if __name__ == '__main__':
    unittest.main()