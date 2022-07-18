import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.period import StrategyRegularInterval
from frestu.optimization.agent.trader.strategy.period.spectrum import OptimizerStrategyRegularInterval
from frestu.evaluation.agent.trader.strategy import Evaluator


class OptimizerStrategyRegularIntervalTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00'],
                ['2020-01-01 17:01:00', 10],
                ['2020-01-01 17:02:00', 20],
                ['2020-01-01 17:03:00', 30],
                ['2020-01-01 17:04:00', 25],
                ['2020-01-01 17:05:00', 15],
                ['2020-01-01 17:06:00', 5],
                ['2020-01-01 17:07:00', 10],
                ['2020-01-01 17:08:00', 30],
                ['2020-01-01 17:09:00', 60],
                ['2020-01-01 17:10:00', 70],
            ],
            columns=['time', 'val'],
        ).set_index('time')

        def calculate_fitness(trader):
            return trader.total_net_profit - 0.01 * trader.total_trades_count

        evaluator = Evaluator(StrategyRegularInterval, calculate_fitness)

        params_default = {
            'period_half': 10,
            'offset': 0,
        }

        self.optimizer = OptimizerStrategyRegularInterval(
            range(2, 5),
            params_default)
        self.optimizer.evaluate = evaluator.create_evaluating(self.df)

    def tearDwon(self):
        pass

    def test_optimize(self):
        self.assertIsNone(self.optimizer.features)
        self.assertIsNone(self.optimizer.params)

        self.optimizer.optimize(self.df)

        features = self.optimizer.features

        period = features['period']
        self.assertEqual(period.iloc[0], 9)
        self.assertEqual(period.iloc[1], 8)
        self.assertEqual(period.iloc[2], 7)

        spectrum = features['spectrum']
        self.assertGreater(spectrum.iloc[0], 8.98)
        self.assertLess(spectrum.iloc[0], 8.99)
        self.assertGreater(spectrum.iloc[1], 16.74)
        self.assertLess(spectrum.iloc[1], 16.75)
        self.assertGreater(spectrum.iloc[2], 14.28)
        self.assertLess(spectrum.iloc[2], 14.29)

        params = self.optimizer.params
        self.assertEqual(params['period_half'], 3)
        self.assertEqual(params['offset'], 1)
        
    def test__calculate_features(self):
        features = self.optimizer._calculate_features(self.df)

        period = features['period']
        self.assertEqual(period.iloc[0], 9)
        self.assertEqual(period.iloc[1], 8)
        self.assertEqual(period.iloc[2], 7)

        spectrum = features['spectrum']
        self.assertGreater(spectrum.iloc[0], 8.98)
        self.assertLess(spectrum.iloc[0], 8.99)
        self.assertGreater(spectrum.iloc[1], 16.74)
        self.assertLess(spectrum.iloc[1], 16.75)
        self.assertGreater(spectrum.iloc[2], 14.28)
        self.assertLess(spectrum.iloc[2], 14.29)
    
    def test__calculate_the_best_params(self):
        features = self.optimizer._calculate_features(self.df)
        params = self.optimizer._calculate_the_best_params(features)
        self.assertEqual(params['period_half'], 3)
        self.assertEqual(params['offset'], 1)
    
    def test__calculate_periods_candidate(self):
        features = self.optimizer._calculate_features(self.df)
        periods_half = self.optimizer._calculate_periods_candidate(features)
        self.assertEqual(periods_half[0], 3)
    
    def test__calculate_offsets_candidate(self):
        features = self.optimizer._calculate_features(self.df)
        periods_half = self.optimizer._calculate_periods_candidate(features)
        offsets, fitnesses = self.optimizer._calculate_offsets_candidate(
            periods_half)
        self.assertEqual(offsets[0], 1)
        self.assertGreater(fitnesses[0], 89.9)
        self.assertLess(fitnesses[0], 90.0)

    def test__select_the_best_ix(self):
        features = self.optimizer._calculate_features(self.df)
        periods_half = self.optimizer._calculate_periods_candidate(features)
        offsets, fitnesses = self.optimizer._calculate_offsets_candidate(
            periods_half)
        ix_best = self.optimizer._select_the_best_ix(fitnesses)
        self.assertEqual(ix_best, 0)
    
    def test_calculate_offset_test(self):
        self.optimizer.optimize(self.df)
        params = self.optimizer.params

        period_half = params['period_half']
        offset_train = params['offset']
        n_rows_train = self.df.shape[0]

        offset_test = OptimizerStrategyRegularInterval.calculate_offset_test(
            period_half, offset_train, n_rows_train)
        
        self.assertEqual(offset_test, 5)


if __name__ == '__main__':
    unittest.main()