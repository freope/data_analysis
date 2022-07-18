import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader import Position
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.probability_calculation import ProbabilityCalculatorMaSlopeMa


class ProbabilityCalculatorMaSlopeMaTests(unittest.TestCase):

    def setUp(self):
        strategy = StrategyGcdc(2, 3)
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 0],
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
        self.positions = Position.create_positions(strategy, self.df)
        self.prob_calculator_sma = ProbabilityCalculatorMaSlopeMa('sma', 2, 3, 1)
        self.prob_calculator_ema = ProbabilityCalculatorMaSlopeMa('ema', 2, 3, 1)
        
    def tearDown(self):
        pass

    def test_calculate(self):
        # sma
        probs = self.prob_calculator_sma.calculate(self.df)
        self.assertTrue(np.isnan(probs.loc['2020-01-01 17:00:00'][0]))
        self.assertGreater(probs.loc['2020-01-01 17:05:00'][0], 0.68)
        self.assertLess(probs.loc['2020-01-01 17:05:00'][0], 0.69)
        self.assertGreater(probs.loc['2020-01-01 17:08:00'][0], -0.01)
        self.assertLess(probs.loc['2020-01-01 17:08:00'][0], 0.01)
        self.assertGreater(probs.loc['2020-01-01 17:10:00'][0], 0.99)
        self.assertLess(probs.loc['2020-01-01 17:10:00'][0], 1.01)

        # ema
        probs = self.prob_calculator_ema.calculate(self.df)
        self.assertTrue(np.isnan(probs.loc['2020-01-01 17:00:00'][0]))
        self.assertGreater(probs.loc['2020-01-01 17:05:00'][0], 0.43)
        self.assertLess(probs.loc['2020-01-01 17:05:00'][0], 0.44)
        self.assertGreater(probs.loc['2020-01-01 17:08:00'][0], 0.67)
        self.assertLess(probs.loc['2020-01-01 17:08:00'][0], 0.68)
        self.assertGreater(probs.loc['2020-01-01 17:10:00'][0], 0.99)
        self.assertLess(probs.loc['2020-01-01 17:10:00'][0], 1.01)


if __name__ == '__main__':
    unittest.main()