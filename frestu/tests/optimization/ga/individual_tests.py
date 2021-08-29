import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga.individual import Individual
from frestu.optimization.ga.crossover import *


class IndividualTests(unittest.TestCase):

    def setUp(self):
        self.gene_c = GeneContinuous(
            minimum=0.0,
            maximum=10,
            dimension=1)
        self.gene_kernel = GeneDiscrete(            
            candidates=['rbf', 'poly', 'linear'],
            crossover=crossover_uniform,
            dimension=1)
        self.gene_feature = GeneDiscrete(
            candidates=[0, 1],
            crossover=crossover_uniform,
            dimension=30)
        self.chromosome_prototype = {
            'C': self.gene_c,
            'kernel': self.gene_kernel,
            'feature': self.gene_feature,
        }
        self.individual = Individual.create(
            self.chromosome_prototype,
            evaluator=lambda chrom: 0,
            learning_rate=1.5)
        self.parent_female = Individual.create(
            self.chromosome_prototype,
            evaluator=lambda chrom: 1,
            learning_rate=1.5)
        self.parent_male = Individual.create(
            self.chromosome_prototype,
            evaluator=lambda chrom: 2,
            learning_rate=1.5)
    
    def tearDown(self):
        pass

    def test_crossover(self):
        # 本来は evaluate で設定される値
        self.individual.evaluate()
        self.parent_female.evaluate()
        self.parent_male.evaluate()

        self.individual.crossover(self.parent_female, self.parent_male)

        learning_rate = 1.5
        c_female = self.parent_female.chromosome['C'].values
        c_male = self.parent_male.chromosome['C'].values
        c_ind = self.individual.chromosome['C'].values
        kernel_female = self.parent_female.chromosome['kernel'].values
        kernel_male = self.parent_male.chromosome['kernel'].values
        kernel_ind = self.individual.chromosome['kernel'].values

        # 今回は male の fitness が female の fitness より大きいので
        c_child = learning_rate * (c_male - c_female) + c_female

        self.assertEqual(c_ind, c_child)
        self.assertTrue(
            kernel_ind == kernel_female or kernel_ind == kernel_male)

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