import os
import sys
import unittest

import pandas as pd
sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.construction.trend import StrategyHaBbMasMstdMss


class StrategyHaBbMasMstdMssTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyHaBbMasMstdMss(4, 0.01, 'sma', 3)
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
        self.assertEqual(len(otsl), 1)
        otl = otsl[0]
        self.assertEqual(otl, '2020-01-01 17:08:00')
        # short
        otss = opening_times[1]
        self.assertEqual(len(otss), 1)
        ots = otss[0]
        self.assertEqual(ots, '2020-01-01 17:06:00')

    def test_calculate_closing_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        closing_times = self.strategy.calculate_closing_times(
            self.df, opening_times)
        # long
        lcts = closing_times[0]
        self.assertEqual(len(lcts), 1)
        lct = lcts[0]
        self.assertEqual(lct, '2020-01-01 17:10:00')
        # short
        scts = closing_times[1]
        self.assertEqual(len(scts), 1)
        sct = scts[0]
        self.assertEqual(sct, '2020-01-01 17:07:00')

    def test_create_positions(self):
        open_positions, closed_positions = \
            self.strategy.create_positions(self.df)
        # open
        self.assertEqual(len(open_positions), 0)
        # closed
        self.assertEqual(len(closed_positions), 2)
        closed_time = closed_positions[0]
        self.assertEqual(closed_time['position_type'], 'long')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:08:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:10:00')
        closed_time = closed_positions[1]
        self.assertEqual(closed_time['position_type'], 'short')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:06:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:07:00')


if __name__ == '__main__':
    unittest.main()