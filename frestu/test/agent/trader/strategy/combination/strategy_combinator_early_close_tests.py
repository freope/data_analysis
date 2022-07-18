import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.combination import StrategyCombinatorEarlyClose
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.strategy.trend import StrategyMau


class StrategyCombinatorEarlyCloseTests(unittest.TestCase):

    def setUp(self):
        self.strategy_0 = StrategyGcdc(2, 3)
        strategy_1 = StrategyMau([2, 3, 4])
        self.strategy = StrategyCombinatorEarlyClose(
            self.strategy_0, strategy_1)
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

    def test_calculate_closing_times(self):
        opening_times = self.strategy_0.calculate_opening_times(self.df)
        closing_times = self.strategy.calculate_closing_times(
            self.df, opening_times)
        # long
        closing_times_long = closing_times[0]
        self.assertEqual(len(closing_times_long), 2)
        self.assertEqual(closing_times_long[0], '2020-01-01 17:05:00')
        self.assertIsNone(closing_times_long[1])
        # short
        closing_times_short = closing_times[1]
        self.assertEqual(len(closing_times_short), 1)
        self.assertEqual(closing_times_short[0], '2020-01-01 17:08:00')


if __name__ == '__main__':
    unittest.main()