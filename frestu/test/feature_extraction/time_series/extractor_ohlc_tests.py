import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorOhlc


class ExtractorOhlcTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorOhlc(2)
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

    def test_extract(self):
        indicators = self.extractor.extract(self.df)
        o = indicators['open']
        h = indicators['high']
        l = indicators['low']
        c = indicators['closing']
        # open
        self.assertTrue(np.isnan(o.loc['2020-01-01 17:00:00']))
        self.assertEqual(o.loc['2020-01-01 17:02:00'], 10)
        self.assertEqual(o.loc['2020-01-01 17:10:00'], 60)
        # high
        self.assertTrue(np.isnan(h.loc['2020-01-01 17:00:00']))
        self.assertEqual(h.loc['2020-01-01 17:02:00'], 20)
        self.assertEqual(h.loc['2020-01-01 17:10:00'], 70)
        # low
        self.assertTrue(np.isnan(l.loc['2020-01-01 17:00:00']))
        self.assertEqual(l.loc['2020-01-01 17:02:00'], 10)
        self.assertEqual(l.loc['2020-01-01 17:10:00'], 60)
        # closing
        self.assertTrue(np.isnan(c.loc['2020-01-01 17:00:00']))
        self.assertEqual(c.loc['2020-01-01 17:02:00'], 20)
        self.assertEqual(c.loc['2020-01-01 17:10:00'], 70)


if __name__ == '__main__':
    unittest.main()
