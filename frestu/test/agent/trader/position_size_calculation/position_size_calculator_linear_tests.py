import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader import Position
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.probability_calculation import ProbabilityCalculatorMaSlopeMa
from frestu.agent.trader.position_size_calculation import PositionSizeCalculatorLinear


class PositionSizeCalculatorLinearTests(unittest.TestCase):

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
        self.probability_calculator = ProbabilityCalculatorMaSlopeMa(
            'sma', 2, 3, 1)
        self.position_size_calculator = PositionSizeCalculatorLinear(3)

    def tearDown(self):
        pass

    def test_calculate(self):
        self.probability_calculator.set_positions_probability(
            self.positions, self.df)
        positions_size = self.position_size_calculator.calculate(
            self.positions, self.df)
        self.assertEqual(positions_size.iloc[0, 0], 0)
        self.assertTrue(np.isnan(positions_size.iloc[1, 0]))
        self.assertGreater(positions_size.iloc[2, 0], 1.9)
        self.assertLess(positions_size.iloc[2, 0], 2.1)


if __name__ == '__main__':
    unittest.main()