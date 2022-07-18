import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.strategy.part import StrategyPartTakeProfit


class StrategyPartTakeProfitTests(unittest.TestCase):

    def setUp(self):
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
        self.strategy_open = StrategyGcdc(2, 3)
        self.strategy_take_profit = StrategyPartTakeProfit(3)
    
    def tearDown(self):
        pass

    def test_calculate_closing_times(self):
        opening_times = self.strategy_open.calculate_opening_times(self.df)
        closing_times = self.strategy_take_profit.calculate_closing_times(
            self.df, opening_times)
        # long
        closing_times_long = closing_times[0]
        self.assertEqual(len(closing_times_long), 2)
        self.assertEqual(closing_times_long[0], '2020-01-01 17:03:00')
        self.assertEqual(closing_times_long[1], '2020-01-01 17:09:00')
        # short
        closing_times_short = closing_times[1]
        self.assertEqual(len(closing_times_short), 1)
        self.assertEqual(closing_times_short[0], '2020-01-01 17:06:00')


if __name__ == '__main__':
    unittest.main()
