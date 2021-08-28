import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga.individual import Individual


class IndividualTests(unittest.TestCase):

    def setUp(self):
        self.gene_c = GeneContinuous(
            minimum = 0.1,
            maximum = 10,
            dimension = 1,
        )
        self.gene_kernel = GeneDiscrete(            
            candidates = ['rbf', 'poly', 'linear'],
            dimension = 1,
        )
        self.gene_feature = GeneDiscrete(
            candidates = [0, 1],
            dimension = 30,
        )
        self.chromosome_prototype = {
            'C': self.gene_c,
            'kernel': self.gene_kernel,
            'feature': self.gene_feature,
        }
    
    def tearDown(self):
        pass

    def test_create(self):
        ind = Individual.create(self.chromosome_prototype, evaluator=None)
        self.assertLessEqual(ind.chromosome['C'].values[0], self.gene_c.maximum)
        self.assertGreaterEqual(
            ind.chromosome['C'].values[0], self.gene_c.minimum)
        self.assertIn(
            ind.chromosome['kernel'].values[0], ['rbf', 'poly', 'linear'])
        self.assertIn(
            ind.chromosome['feature'].values[0], [0, 1])
        self.assertEqual(
            len(ind.chromosome['feature'].values), self.gene_feature.dimension)


if __name__ == '__main__':
    unittest.main()