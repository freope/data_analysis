import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.strategy.trend.strategy_mau_dependent_close import StrategyMauDependentClose


class StrategyCombinatorOpenAndCloseTests(unittest.TestCase):

    def setUp(self):
        self.open_strategy = StrategyGcdc(2, 3)
        self.close_strategy = StrategyMauDependentClose([2, 3, 4])
        self.strategy = StrategyCombinatorOpenAndClose(
            self.open_strategy, self.close_strategy)
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
        ots = self.strategy.calculate_opening_times(self.df)
        ots_open = self.open_strategy.calculate_opening_times(self.df)
        # long
        ots_long = ots[0]
        ots_open_long = ots_open[0]
        for ot, ot_open in zip(ots_long, ots_open_long):
            self.assertEqual(ot, ot_open)
        # short
        ots_short = ots[1]
        ots_open_short = ots_open[1]
        for ot, ot_open in zip(ots_short, ots_open_short):
            self.assertEqual(ot, ot_open)
    
    def test_calculate_closing_times(self):
        ots = self.strategy.calculate_opening_times(self.df)
        cts = self.strategy.calculate_closing_times(self.df, ots)

        ots_open = self.open_strategy.calculate_opening_times(self.df)
        cts_close = self.close_strategy.calculate_closing_times(
            self.df, ots_open)

        self.assertEqual(cts, cts_close)

    def test_calculate_times(self):
        open_times, close_times = self.strategy.calculate_times(self.df)

        ots_open = self.open_strategy.calculate_opening_times(self.df)

        cts_close = self.close_strategy.calculate_closing_times(
            self.df, ots_open)

        self.assertEqual(open_times, ots_open)
        self.assertEqual(close_times, cts_close)


if __name__ == '__main__':
    unittest.main()
