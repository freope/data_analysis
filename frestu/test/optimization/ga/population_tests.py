import os
import random
import sys
import unittest

sys.path.append(os.path.abspath('..'))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga import Individual
from frestu.optimization.ga import Population
from frestu.optimization.ga.crossover import *
from frestu.optimization.ga.selection import *


class PopulationTests(unittest.TestCase):

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
        self.individual_prototype = Individual.create(
            self.chromosome_prototype,
            evaluate=lambda chrom: random.random(),
            learning_rate=1.5)
        self.population = Population.create(
            self.individual_prototype,
            select_roulette,
            pop_size=10).realize()

    def tearDown(self):
        pass

    def test_evaluate(self):
        ind = self.population.individuals[0]
        # evaluate() 前の fitness は None
        self.assertEqual(ind.fitness, None)
        # evaluate() を実行して
        self.population.evaluate()
        # evaluate() 後の fitness は None でない
        self.assertNotEqual(ind.fitness, None)
        # fitness の降順に並んでいる
        for i in range(len(self.population.individuals)-1):
            ind1 = self.population.individuals[i]            
            ind2 = self.population.individuals[i+1]
            self.assertGreaterEqual(ind1.fitness, ind2.fitness)

    def test_create(self):
        for ind in self.population.individuals:
            self.assertTrue(isinstance(ind, Individual))
        self.assertEqual(len(self.population.individuals), 10)


if __name__ == '__main__':
    unittest.main()