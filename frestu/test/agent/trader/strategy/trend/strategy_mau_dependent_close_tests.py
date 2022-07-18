import os
import sys
import unittest

import math
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.trend.strategy_mau_dependent_close import StrategyMauDependentClose


class StrategyMauDependentCloseTests(unittest.TestCase):
    """
    StrategyIndependentClose を継承したクラスの実装練習用。
    もともとは、StrategyContinuousIndicator を継承して実装するもの。
    """
    def setUp(self):
        self.strategy = StrategyMauDependentClose(windows=[2, 3, 4])
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
        opening_times = self.strategy.calculate_opening_times(self.df)
        # long
        otsl = opening_times[0]
        self.assertEqual(len(otsl), 2)
        otl = otsl[0]
        self.assertEqual(otl, '2020-01-01 17:04:00')
        otl = otsl[1]
        self.assertEqual(otl, '2020-01-01 17:08:00')
        # short
        otss = opening_times[1]
        self.assertEqual(len(otss), 1)
        ots = otss[0]
        self.assertEqual(ots, '2020-01-01 17:06:00')

    def test_calculate_closing_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        corresponding_closing_times = self.strategy.calculate_closing_times(
                self.df, opening_times)
        # NOTE: Independent とここが異なる。
        # long
        lcts = corresponding_closing_times[0]
        self.assertEqual(len(lcts), 2)
        lct = lcts[0]
        self.assertEqual(lct, '2020-01-01 17:05:00')
        lct = lcts[1]
        self.assertIsNone(lct)
        # short
        scts = corresponding_closing_times[1]
        self.assertEqual(len(scts), 1)
        sct = scts[0]
        self.assertEqual(sct, '2020-01-01 17:08:00')

    def test_create_positions(self):
        open_positions, closed_positions = \
            self.strategy.create_positions(self.df)
        # open
        self.assertEqual(len(open_positions), 1)
        open_time = open_positions[0]
        self.assertEqual(open_time['position_type'], 'long')
        self.assertEqual(open_time['opening_time'], '2020-01-01 17:08:00')
        self.assertIsNone(open_time['closing_time'])
        # closed
        self.assertEqual(len(closed_positions), 2)
        closed_time = closed_positions[0]
        self.assertEqual(closed_time['position_type'], 'long')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:04:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:05:00')
        closed_time = closed_positions[1]
        self.assertEqual(closed_time['position_type'], 'short')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:06:00')

    def test_calculate_open_indicators(self):
        indicators = self.strategy.calculate_open_indicators(self.df)
        # ma_2
        self.assertEqual(indicators.loc['2020-01-01 17:04:00', 'ma_2'], 2.5)
        self.assertEqual(indicators.loc['2020-01-01 17:09:00', 'ma_2'], 25.0)
        # ma_3
        self.assertEqual(indicators.loc['2020-01-01 17:04:00', 'ma_3'], 5.0)
        self.assertGreater(indicators.loc['2020-01-01 17:09:00', 'ma_3'], 18)
        self.assertLess(indicators.loc['2020-01-01 17:09:00', 'ma_3'], 19)
        # ma_4
        self.assertEqual(indicators.loc['2020-01-01 17:04:00', 'ma_4'], 6.25)
        self.assertEqual(indicators.loc['2020-01-01 17:09:00', 'ma_4'], 11.25)


if __name__ == '__main__':
    unittest.main()