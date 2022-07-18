import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.period import StrategyRegularIntervalAndSlope


class StrategyRegularIntervalAndSlopeTests(unittest.TestCase):

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
        self.strategy = StrategyRegularIntervalAndSlope(3, 1, 'sma', 2)

    def tearDown(self):
        pass

    def test_calculate_open_indicators(self):
        slope_ma, indicator_ri = self.strategy.calculate_open_indicators(
            self.df)

        # slope_ma
        self.assertTrue(np.isnan(slope_ma.loc['2020-01-01 17:00:00'][0]))
        self.assertEqual(slope_ma.loc['2020-01-01 17:03:00'][0], 10)
        self.assertEqual(slope_ma.loc['2020-01-01 17:10:00'][0], 20)

        # indicator_ri
        self.assertFalse(indicator_ri.iloc[0])
        self.assertTrue(indicator_ri.iloc[1])
        self.assertTrue(indicator_ri.iloc[2])
        self.assertTrue(indicator_ri.iloc[3])
        self.assertFalse(indicator_ri.iloc[4])
        self.assertFalse(indicator_ri.iloc[5])
        self.assertFalse(indicator_ri.iloc[6])
        self.assertTrue(indicator_ri.iloc[7])
        self.assertTrue(indicator_ri.iloc[8])
        self.assertTrue(indicator_ri.iloc[9])
        self.assertFalse(indicator_ri.iloc[10])
    
    def test_convert_open_indicators(self):
        indicators = self.strategy.calculate_open_indicators(
            self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicators, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicators, 'short')
        # long
        self.assertFalse(can_open_long.loc['2020-01-01 17:02:00'])
        self.assertTrue(can_open_long.loc['2020-01-01 17:03:00'])
        self.assertFalse(can_open_long.loc['2020-01-01 17:07:00'])
        self.assertTrue(can_open_long.loc['2020-01-01 17:08:00'])
        # short
        self.assertFalse(can_open_short.loc['2020-01-01 17:04:00'])
        self.assertTrue(can_open_short.loc['2020-01-01 17:05:00'])


if __name__ == '__main__':
    unittest.main()