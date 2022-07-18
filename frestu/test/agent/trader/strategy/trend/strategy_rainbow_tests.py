import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend import StrategyRainbow


class StrategyRainbowTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyRainbow('ema', 10, 20, 35)
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
        # long
        self.assertTrue(indicators.loc['2020-01-01 17:06:00', 'long'])
        # short
        self.assertFalse(indicators.loc['2020-01-01 17:06:00', 'short'])
    
    def test_calculate_close_indicators(self):
        indicators = self.strategy.calculate_close_indicators(self.df)
        # long
        self.assertFalse(indicators.loc['2020-01-01 17:05:00', 'long'])
        self.assertTrue(indicators.loc['2020-01-01 17:06:00', 'long'])
        self.assertTrue(indicators.loc['2020-01-01 17:07:00', 'long'])        
        # short
        self.assertTrue(indicators.loc['2020-01-01 17:05:00', 'short'])
        self.assertTrue(indicators.loc['2020-01-01 17:06:00', 'short'])
        self.assertTrue(indicators.loc['2020-01-01 17:07:00', 'short'])
        
    def test_calculate_opening_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        # long
        otsl = opening_times[0]
        self.assertEqual(len(otsl), 1)
        otl = otsl[0]
        self.assertEqual(otl, '2020-01-01 17:06:00')
        # short
        otss = opening_times[1]
        self.assertEqual(len(otss), 0)
    
    def test_calculate_closing_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        closing_times = self.strategy.calculate_closing_times(
            self.df, opening_times)
        # long
        lcts = closing_times[0]
        self.assertEqual(len(lcts), 1)
        lct = lcts[0]
        # NOTE: エントリーとエクジットが同時刻だと、エクジットが無視されることに注意。
        self.assertIsNone(lct)
        # short
        scts = closing_times[1]
        self.assertEqual(len(scts), 0)
    
    def test_create_positions(self):
        open_positions, closed_positions = \
            self.strategy.create_positions(self.df)
        # open
        self.assertEqual(len(open_positions), 1)
        open_time = open_positions[0]
        self.assertEqual(open_time['position_type'], 'long')
        self.assertEqual(open_time['opening_time'], '2020-01-01 17:06:00')
        self.assertIsNone(open_time['closing_time'])
        # closed
        self.assertEqual(len(closed_positions), 0)


if __name__ == '__main__':
    unittest.main()