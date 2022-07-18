import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.oscillator import StrategyDmiDiAdx


class StrategyDmiDiAdxTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyDmiDiAdx(3, 4, 3, 0.4)
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
        indicators = self.strategy.calculate_open_indicators(self.df)
        p_di = indicators['+DI']
        m_di = indicators['-DI']
        adx = indicators['ADX']
        # +DI
        self.assertTrue(np.isnan(p_di.loc['2020-01-01 17:04:00']))
        self.assertGreater(p_di.loc['2020-01-01 17:05:00'], 0.15)
        self.assertLess(p_di.loc['2020-01-01 17:05:00'], 0.16)
        self.assertGreater(p_di.loc['2020-01-01 17:10:00'], 0.43)
        self.assertLess(p_di.loc['2020-01-01 17:10:00'], 0.45)
        # -DI
        self.assertTrue(np.isnan(m_di.loc['2020-01-01 17:04:00']))
        self.assertGreater(m_di.loc['2020-01-01 17:05:00'], 0.07)
        self.assertLess(m_di.loc['2020-01-01 17:05:00'], 0.08)
        self.assertEqual(m_di.loc['2020-01-01 17:10:00'], 0.0)
        # ADX
        self.assertTrue(np.isnan(adx.loc['2020-01-01 17:06:00']))
        self.assertGreater(adx.loc['2020-01-01 17:07:00'], 0.50)
        self.assertLess(adx.loc['2020-01-01 17:07:00'], 0.52)
        self.assertGreater(adx.loc['2020-01-01 17:10:00'], 0.54)
        self.assertLess(adx.loc['2020-01-01 17:10:00'], 0.55)

    def test_convert_open_indicators(self):
        indicators = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicators, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicators, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:08:00'])
        self.assertTrue(can_open_long['2020-01-01 17:09:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:06:00'])
        self.assertTrue(can_open_short['2020-01-01 17:07:00'])


if __name__ == '__main__':
    unittest.main()