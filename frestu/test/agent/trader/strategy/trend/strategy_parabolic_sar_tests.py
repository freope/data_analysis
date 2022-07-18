import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend import StrategyParabolicSar


class StrategyParabolicSarTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyParabolicSar(0.02, 0.2)
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
        indicator = self.strategy.calculate_open_indicators(self.df)
        self.assertEqual(indicator.loc['2020-01-01 17:00:00'], 0)
        self.assertGreater(indicator.loc['2020-01-01 17:04:00'], 20)
        self.assertLess(indicator.loc['2020-01-01 17:04:00'], 21)
        self.assertGreater(indicator.loc['2020-01-01 17:07:00'], -20)
        self.assertLess(indicator.loc['2020-01-01 17:07:00'], -18)

    def test_convert_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:00:00'])
        self.assertTrue(can_open_long['2020-01-01 17:01:00'])
        self.assertFalse(can_open_long['2020-01-01 17:07:00'])
        self.assertTrue(can_open_long['2020-01-01 17:08:00'])
        # short        
        self.assertFalse(can_open_short['2020-01-01 17:05:00'])
        self.assertTrue(can_open_short['2020-01-01 17:06:00'])


if __name__ == '__main__':
    unittest.main()