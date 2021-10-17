import os
import sys
import unittest

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.gene import GeneContinuous


class GeneContinuousTests(unittest.TestCase):

    def setUp(self):
        self.gene = GeneContinuous(
            minimum=1.0,
            maximum=5.0,
            dimension=3,
            mutate_probability=0.01)
        self.gene_partner = GeneContinuous(
            minimum=1.0,
            maximum=5.0,
            dimension=3,
            mutate_probability=0.01)
        
    def tearDown(self):
        pass

    def test_dimension(self):
        self.assertEqual(self.gene.dimension, 3)

    def test_minimum(self):
        self.assertEqual(self.gene.minimum, 1.0)

    def test_maximum(self):
        self.assertEqual(self.gene.maximum, 5.0)

    def test_get_mutate_probability(self):
        self.assertEqual(self.gene.mutate_probability, 0.01)
    
    def test_set_mutate_probability(self):
        self.gene.mutate_probability = 0.1
        self.assertEqual(self.gene.mutate_probability, 0.1)

    def test_mutate_when_probability_is_zero(self):
        original_values = self.gene.realize().values.copy()

        # 全ての成分が突然変異しない場合
        self.gene.mutate_probability = 0.0
        mutated_values = self.gene.mutate().values

        # 全ての成分が変化していない
        self.assertEqual(list(original_values), list(mutated_values))

    def test_mutate_when_probability_is_one(self):
        original_values = self.gene.realize().values.copy()

        # 全ての成分が突然変異する場合
        self.gene.mutate_probability = 1.0
        mutated_values = self.gene.mutate().values

        # 変化している成分がある
        # HACK: 突然変異前後で偶々全ての成分の値が同じになれば、失敗することに注意
        self.assertNotEqual(list(original_values), list(mutated_values))

    def test_crossover(self):
        self.gene.realize()
        self.gene_partner.realize()
        gene_child = self.gene.crossover(
            self.gene_partner,
            fitness_self=10, fitness_partner=20,
            learning_rate=0.5)
        child_values = (self.gene_partner.values + self.gene.values) * 0.5
        self.assertEqual(list(gene_child.values), list(child_values))

    def test_realize(self):
        realized = self.gene.realize().values

        # サイズが合っているか
        self.assertEqual(len(realized), self.gene.dimension)

        # 内容が合っているか
        for val in realized:
            self.assertGreaterEqual(val, self.gene.minimum)
            self.assertLessEqual(val, self.gene.maximum)


if __name__ == '__main__':
    unittest.main()