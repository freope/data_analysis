import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend import StrategyBbCrossMaSigma


class StrategyBbCrossMaSigmaTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyBbCrossMaSigma('ema', 3, 'sma', 2, 1)
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
    
    def test_calculate_open_indicators(self):
        indr_l, indr_s = self.strategy.calculate_open_indicators(self.df)

        # long
        self.assertTrue(np.isnan(indr_l.loc['2020-01-01 17:00:00']))
        self.assertGreater(indr_l.loc['2020-01-01 17:01:00'], -7.08)
        self.assertLess(indr_l.loc['2020-01-01 17:01:00'], -7.07)
        self.assertGreater(indr_l.loc['2020-01-01 17:10:00'], -17.0)
        self.assertLess(indr_l.loc['2020-01-01 17:10:00'], -16.9)
        # short
        self.assertTrue(np.isnan(indr_s.loc['2020-01-01 17:00:00']))
        self.assertGreater(indr_s.loc['2020-01-01 17:01:00'], 7.07)
        self.assertLess(indr_s.loc['2020-01-01 17:01:00'], 7.08)
        self.assertGreater(indr_s.loc['2020-01-01 17:10:00'], -2.9)
        self.assertLess(indr_s.loc['2020-01-01 17:10:00'], -2.8)

    def test_convert_indicators(self):
        indicators = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicators, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicators, 'short')
        # short
        self.assertFalse(can_open_short['2020-01-01 17:03:00'])
        self.assertTrue(can_open_short['2020-01-01 17:04:00'])
        self.assertFalse(can_open_short['2020-01-01 17:05:00'])
        self.assertFalse(can_open_short['2020-01-01 17:09:00'])
        self.assertTrue(can_open_short['2020-01-01 17:10:00'])


if __name__ == '__main__':
    unittest.main()