import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend import StrategyBbMasmMstdMssm


class StrategyBbMasmMstdMssmTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyBbMasmMstdMssm(0.1, 'sma', 2, 2, 2)
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
        ma_diff, sigma, ma_diff_sigma = \
            self.strategy.calculate_open_indicators(self.df)
        # ma_diff
        self.assertTrue(np.isnan(ma_diff.loc['2020-01-01 17:00:00'][0]))
        self.assertEqual(ma_diff.loc['2020-01-01 17:03:00'][0], 10)
        self.assertEqual(ma_diff.loc['2020-01-01 17:10:00'][0], 22.5)
        # sigma
        self.assertTrue(np.isnan(sigma.loc['2020-01-01 17:00:00'][0]))
        self.assertGreater(sigma.loc['2020-01-01 17:01:00'][0], 7.0)
        self.assertLess(sigma.loc['2020-01-01 17:01:00'][0], 7.1)
        self.assertGreater(sigma.loc['2020-01-01 17:09:00'][0], 21)
        self.assertLess(sigma.loc['2020-01-01 17:09:00'][0], 22)
        # ma_diff_sigma
        self.assertTrue(np.isnan(ma_diff_sigma.loc['2020-01-01 17:00:00'][0]))
        self.assertEqual(ma_diff_sigma.loc['2020-01-01 17:03:00'][0], 0)
        self.assertGreater(ma_diff_sigma.loc['2020-01-01 17:09:00'][0], 8.8)
        self.assertLess(ma_diff_sigma.loc['2020-01-01 17:09:00'][0], 8.9)
    
    def test_convert_indicators(self):
        indicators = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicators, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicators, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:07:00'])
        self.assertTrue(can_open_long['2020-01-01 17:08:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:05:00'])
        self.assertTrue(can_open_short['2020-01-01 17:06:00'])


if __name__ == '__main__':
    unittest.main()