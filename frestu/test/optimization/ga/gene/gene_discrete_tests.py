import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.crossover import *


class GeneDiscreteTests(unittest.TestCase):

    def setUp(self):
        self.gene = GeneDiscrete(
            candidates=[0, 1, 2, 3, 4],
            crossover=crossover_uniform,
            dimension=3,
            mutate_probability=0.01)
        self.gene_replacement_false = GeneDiscrete(
            candidates=[0, 1, 2, 3, 4],
            crossover=None,
            dimension=5,
            mutate_probability=0.01,
            replacement = False)
        self.gene_partner = GeneDiscrete(
            candidates=[0, 1, 2, 3, 4],
            crossover=crossover_uniform,
            dimension=3,
            mutate_probability=0.01)
    
    def tearDown(self):
        pass
    
    def test_dimension(self):
        self.assertEqual(self.gene.dimension, 3)

    def test_candidates(self):
        self.assertEqual(self.gene.candidates, [0, 1, 2, 3, 4])

    def test_get_mutate_probability(self):
        self.assertEqual(self.gene.mutate_probability, 0.01)
    
    def test_set_mutate_probability(self):
        self.gene.mutate_probability = 0.1
        self.assertEqual(self.gene.mutate_probability, 0.1)

    def test_mutate_replacement_true_when_probability_is_zero(self):
        original_values = self.gene.realize().values.copy()

        # 全ての成分が突然変異しない場合
        self.gene.mutate_probability = 0.0
        mutated_values = self.gene.mutate().values

        # 全ての成分が変化していない
        self.assertEqual(list(original_values), list(mutated_values))

    def test_mutate_replacement_true_when_probability_is_one(self):
        original_values = self.gene.realize().values.copy()

        # 全ての成分が突然変異しない場合
        self.gene.mutate_probability = 1.0
        mutated_values = self.gene.mutate().values

        # 変化している成分がある
        # HACK: 突然変異前後で偶々全ての成分の値が同じになれば、失敗することに注意
        self.assertNotEqual(list(original_values), list(mutated_values))

    def test_mutate_replacement_false_when_probability_is_zero(self):
        original_values = self.gene_replacement_false.realize().values.copy()

        # 全ての成分が突然変異しない場合
        self.gene_replacement_false.mutate_probability = 0.0
        mutated_values = self.gene_replacement_false.mutate().values

        # 全ての成分が変化していない
        self.assertEqual(list(original_values), list(mutated_values))

    def test_mutate_replacement_false_when_probability_is_one(self):
        original_values = self.gene_replacement_false.realize().values.copy()

        # 全ての成分が突然変異しない場合
        self.gene_replacement_false.mutate_probability = 1.0
        mutated_values = self.gene_replacement_false.mutate().values

        # 変化している成分がある
        # HACK: 突然変異前後で偶々全ての成分の値が同じになれば、失敗することに注意
        self.assertNotEqual(list(original_values), list(mutated_values))

        # 和が同じになることで、重複がないことを確認する
        # HACK: 偶々和が同じになった場合は、テストできていないことになる。
        self.assertEqual(original_values.sum(), mutated_values.sum())

    def test_crossover(self):
        self.gene.realize()
        self.gene_partner.realize()
        gene_child = self.gene.crossover(
            self.gene_partner,
            fitness_self=10, fitness_partner=20,
            learning_rate=0.5)
        self.assertEqual(len(gene_child.values), len(self.gene.values))

    def test_realize(self):
        realized = self.gene.realize().values

        # サイズが合っているか
        self.assertEqual(len(realized), self.gene.dimension)

        # 内容が合っているか
        for val in realized:
            self.assertIn(val, self.gene.candidates)


if __name__ == '__main__':
    unittest.main()