import os
import sys
import unittest

import pandas as pd

from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

sys.path.append(os.path.abspath(".."))
from frestu.optimization.ga.evaluation import EvaluatorRegression
from frestu.optimization.ga.evaluation import ObserverAbstract
from frestu.optimization.ga.gene import GeneDiscrete
from frestu.optimization.ga.gene import GeneContinuous
from frestu.optimization.ga.crossover import crossover_uniform


class EvaluatorRegressionTests(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_create_evaluating_by_cross_validation(self):
        model_class = Ridge

        X = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1, 0],
                ['2020-01-01 17:01:00', 2, 1],
                ['2020-01-01 17:02:00', 3, 2],
                ['2020-01-01 17:03:00', 4, 3],
                ['2020-01-01 17:04:00', 5, 4],
                ['2020-01-01 17:05:00', 6, 5],
            ],
            columns=['time', 'val1', 'val2'],
        ).set_index('time')

        y = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 4],
                ['2020-01-01 17:01:00', 7],
                ['2020-01-01 17:02:00', 10],
                ['2020-01-01 17:03:00', 13],
                ['2020-01-01 17:04:00', 16],
                ['2020-01-01 17:05:00', 19],
            ],
            columns=['time', 'val'],
        ).set_index('time')

        def calculate_score(y, y_pred, **kwargs):
            return mean_squared_error(y, y_pred)

        def translate_chromosome(chrom):
            feature_selection_params = chrom.pop('feature').values == 1
            model_hyper_params = dict([
                (gene_name, gene.values) for gene_name, gene in chrom.items()])
            return model_hyper_params, feature_selection_params

        def convert_scores_to_fitness(scores):
            return -sum(scores)

        class ParameterObserver(ObserverAbstract):
            def observe(self, evaluator):
                chrom = evaluator.chromosome
                # print('alpha: {}'.format(chrom['alpha'].values))

        evaluator = EvaluatorRegression(
            model_class,
            X, y,
            translate_chromosome,
            calculate_score,
            convert_scores_to_fitness)
        evaluator.add_observer(ParameterObserver())
        evaluate = evaluator.create_evaluating_by_cross_validation(n_splits=3)

        gene_alpha = GeneContinuous(
            minimum=0,
            maximum=1000,
            dimension=1).realize()
        gene_feature = GeneDiscrete(
            candidates=[0, 1],
            crossover=crossover_uniform,
            dimension=2).realize()
        chromosome_prototype = {
            'alpha': gene_alpha,
            'feature': gene_feature}

        fitness = evaluate(chromosome_prototype)

        # エラーなく動く事だけ確認。
        self.assertLess(fitness, 0)


if __name__ == '__main__':
    unittest.main()