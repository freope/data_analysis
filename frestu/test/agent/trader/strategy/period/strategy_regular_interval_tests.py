import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyRegularIntervalTests(unittest.TestCase):

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
        self.strategy = StrategyRegularInterval(3, 1)

    def tearDown(self):
        pass

    def test_calculate_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        self.assertFalse(indicator.iloc[0])
        self.assertTrue(indicator.iloc[1])
        self.assertTrue(indicator.iloc[2])
        self.assertTrue(indicator.iloc[3])
        self.assertFalse(indicator.iloc[4])
        self.assertFalse(indicator.iloc[5])
        self.assertFalse(indicator.iloc[6])
        self.assertTrue(indicator.iloc[7])
        self.assertTrue(indicator.iloc[8])
        self.assertTrue(indicator.iloc[9])
        self.assertFalse(indicator.iloc[10])
        # print(indicator)
    
    def test_convert_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long.iloc[0])
        self.assertTrue(can_open_long.iloc[1])
        self.assertTrue(can_open_long.iloc[2])
        self.assertTrue(can_open_long.iloc[3])
        self.assertFalse(can_open_long.iloc[4])
        self.assertFalse(can_open_long.iloc[5])
        self.assertFalse(can_open_long.iloc[6])
        self.assertTrue(can_open_long.iloc[7])
        self.assertTrue(can_open_long.iloc[8])
        self.assertTrue(can_open_long.iloc[9])
        self.assertFalse(can_open_long.iloc[10])
        # short
        self.assertFalse(can_open_short.iloc[0])
        self.assertFalse(can_open_short.iloc[1])
        self.assertFalse(can_open_short.iloc[2])
        self.assertFalse(can_open_short.iloc[3])
        self.assertTrue(can_open_short.iloc[4])
        self.assertTrue(can_open_short.iloc[5])
        self.assertTrue(can_open_short.iloc[6])
        self.assertFalse(can_open_short.iloc[7])
        self.assertFalse(can_open_short.iloc[8])
        self.assertFalse(can_open_short.iloc[9])
        self.assertTrue(can_open_short.iloc[10])


if __name__ == '__main__':
    unittest.main()