import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader import Position
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.position_size_calculation import PositionSizeCalculatorUniform


class PositionSizeCalculatorUniformTests(unittest.TestCase):

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
        self.position_size_calculator = PositionSizeCalculatorUniform(3)

    def tearDown(self):
        pass

    def test_set_positions_size(self):
        for position in self.positions:
            self.assertEqual(position.position_size, 1)
        self.position_size_calculator.set_positions_size(
            self.positions, self.df)
        for position in self.positions:
            self.assertEqual(position.position_size, 3)

    def test_calculate(self):
        positions_size = self.position_size_calculator.calculate(
            self.positions, self.df)
        self.assertEqual(positions_size.loc['2020-01-01 17:00:00'][0], 3)
        self.assertEqual(positions_size.loc['2020-01-01 17:10:00'][0], 3)


if __name__ == '__main__':
    unittest.main()