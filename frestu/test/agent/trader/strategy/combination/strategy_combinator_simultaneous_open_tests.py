import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.combination import StrategyCombinatorSimultaneousOpen
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.strategy.trend import StrategyMau


class StrategyCombinatorSimultaneousOpenTests(unittest.TestCase):

    def setUp(self):
        strategy_0 = StrategyGcdc(2, 3)
        strategy_1 = StrategyMau([2, 3, 4])
        self.strategy = strategy = StrategyCombinatorSimultaneousOpen(
            1, strategy_0, strategy_1)
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

    def test_calculate_opening_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        # long
        otsl = opening_times[0]
        self.assertEqual(len(otsl), 1)
        otl = otsl[0]
        self.assertEqual(otl, '2020-01-01 17:08:00')
        # short
        otss = opening_times[1]
        self.assertEqual(len(otss), 1)
        ots = otss[0]
        self.assertEqual(ots, '2020-01-01 17:06:00')


if __name__ == '__main__':
    unittest.main()