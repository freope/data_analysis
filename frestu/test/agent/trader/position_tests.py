import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader import Position
from frestu.agent.trader.strategy.trend import StrategyMau


class PositionTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyMau(windows=[2, 3, 4])
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
    
    def tearDown(self):
        pass

    def test_create_positions(self):
        positions = Position.create_positions(self.strategy, self.df)
        self.assertEqual(
            str(positions[0]),
            '2020-01-01 17:08:00,None,30,None,long')
        self.assertEqual(
            str(positions[1]),
            '2020-01-01 17:04:00,2020-01-01 17:05:00,25,15,long')
        self.assertEqual(
            str(positions[2]),
            '2020-01-01 17:06:00,2020-01-01 17:08:00,5,30,short')


if __name__ == '__main__':
    unittest.main()