import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.cross import StrategyDfma


class StrategyDfmaTests(unittest.TestCase):

    def setUp(self):
        self.strategy_dfsma = StrategyDfma('sma', 2)
        self.strategy_dfema = StrategyDfma('ema', 2)
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
        # dfsma
        indicator = self.strategy_dfsma.calculate_open_indicators(self.df)
        self.assertTrue(np.isnan(indicator.loc['2020-01-01 17:00:00']))
        self.assertEqual(indicator.loc['2020-01-01 17:01:00'], 5.0)
        self.assertEqual(indicator.loc['2020-01-01 17:09:00'], 15.0)
        
        # dfema
        indicator = self.strategy_dfema.calculate_open_indicators(self.df)
        self.assertEqual(indicator.loc['2020-01-01 17:00:00'], 0.0)
        self.assertGreater(indicator.loc['2020-01-01 17:01:00'], 3.3)
        self.assertLess(indicator.loc['2020-01-01 17:01:00'], 3.4)
        self.assertGreater(indicator.loc['2020-01-01 17:09:00'], 12.2)
        self.assertLess(indicator.loc['2020-01-01 17:09:00'], 12.3)
    
    def test_convert_open_indicators(self):
        # dfsma
        indicator = self.strategy_dfsma.calculate_open_indicators(self.df)
        can_open_long = self.strategy_dfsma.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy_dfsma.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:00:00'])
        self.assertTrue(can_open_long['2020-01-01 17:01:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:03:00'])
        self.assertTrue(can_open_short['2020-01-01 17:04:00'])

        # dfema
        indicator = self.strategy_dfema.calculate_open_indicators(self.df)
        can_open_long = self.strategy_dfema.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy_dfema.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:00:00'])
        self.assertTrue(can_open_long['2020-01-01 17:01:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:03:00'])
        self.assertTrue(can_open_short['2020-01-01 17:04:00'])


if __name__ == '__main__':
    unittest.main()