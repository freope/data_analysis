import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.construction.oscillator import StrategyMacdReverseStopLossRatio


class StrategyMacdReverseStopLossRatioTests(unittest.TestCase):

    def setUp(self):
        self.strategy = StrategyMacdReverseStopLossRatio(2, 3, 0.01)
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
        self.assertEqual(otl, '2020-01-01 17:05:00')
        # short
        otss = opening_times[1]
        self.assertEqual(len(otss), 2)
        ots = otss[0]
        self.assertEqual(ots, '2020-01-01 17:01:00')
        ots = otss[1]
        self.assertEqual(ots, '2020-01-01 17:08:00')

    def test_calculate_closing_times(self):
        opening_times = self.strategy.calculate_opening_times(self.df)
        closing_times = self.strategy.calculate_closing_times(
            self.df, opening_times)
        # long
        lcts = closing_times[0]
        self.assertEqual(len(lcts), 1)
        lct = lcts[0]
        self.assertEqual(lct, '2020-01-01 17:06:00')
        # short
        scts = closing_times[1]
        self.assertEqual(len(scts), 2)
        sct = scts[0]
        self.assertEqual(sct, '2020-01-01 17:02:00')
        sct = scts[1]
        self.assertEqual(sct, '2020-01-01 17:09:00')

    def test_create_positions(self):
        open_positions, closed_position = \
            self.strategy.create_positions(self.df)
        # open
        self.assertEqual(len(open_positions), 0)
        # closed
        self.assertEqual(len(closed_position), 3)
        closed_time = closed_position[0]
        self.assertEqual(closed_time['position_type'], 'long')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:05:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:06:00')
        closed_time = closed_position[1]
        self.assertEqual(closed_time['position_type'], 'short')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:01:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:02:00')
        closed_time = closed_position[2]
        self.assertEqual(closed_time['position_type'], 'short')
        self.assertEqual(closed_time['opening_time'], '2020-01-01 17:08:00')
        self.assertEqual(closed_time['closing_time'], '2020-01-01 17:09:00')


if __name__ == '__main__':
    unittest.main()