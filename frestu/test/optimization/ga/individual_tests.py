import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga import Individual
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
            evaluate=lambda chrom: 0,
            learning_rate=1.5).realize()
        self.partner = Individual.create(
            self.chromosome_prototype,
            evaluate=lambda chrom: 1,
            learning_rate=1.5).realize()
    
    def tearDown(self):
        pass

    def test_crossover(self):
        # 本来は evaluate で設定される値
        self.individual.evaluate()
        self.partner.evaluate()

        child = self.individual.crossover(self.partner)

        learning_rate = 1.5
        c_ind = self.individual.chromosome['C'].values
        c_partner = self.partner.chromosome['C'].values
        c_child = child.chromosome['C'].values
        kernel_ind = self.individual.chromosome['kernel'].values
        kernel_partner = self.partner.chromosome['kernel'].values
        kernel_child = child.chromosome['kernel'].values

        # 今回は partner の fitness が individual の fitness より大きいので
        c_child_answer = learning_rate * (c_partner - c_ind) + c_ind
        # 最小値以上最大以下に制限する
        c_child_answer[
            c_child_answer < self.gene_c.minimum] = self.gene_c.minimum
        c_child_answer[
            self.gene_c.maximum < c_child_answer] = self.gene_c.maximum

        self.assertEqual(c_child, c_child_answer)
        self.assertTrue(
            kernel_child == kernel_ind or kernel_child == kernel_partner)

    def test_create(self):
        ind = Individual.create(
            self.chromosome_prototype, evaluate=None).realize()
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