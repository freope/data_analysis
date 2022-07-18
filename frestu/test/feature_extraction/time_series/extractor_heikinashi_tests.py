import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorHeikinashi


class ExtractorHeikinashiTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorHeikinashi(2)
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
        feature = self.extractor.extract(self.df)
        # open
        ha_open = feature['ha_open']
        self.assertTrue(np.isnan(ha_open.loc['2020-01-01 17:01:00']))
        self.assertEqual(ha_open.loc['2020-01-01 17:02:00'], 5)
        self.assertGreater(ha_open.loc['2020-01-01 17:10:00'], 30)
        self.assertLess(ha_open.loc['2020-01-01 17:10:00'], 31)
        # high
        ha_high = feature['ha_high']
        self.assertTrue(np.isnan(ha_high.loc['2020-01-01 17:00:00']))
        self.assertEqual(ha_high.loc['2020-01-01 17:01:00'], 10)
        self.assertEqual(ha_high.loc['2020-01-01 17:10:00'], 70)
        # low
        ha_low = feature['ha_low']
        self.assertTrue(np.isnan(ha_low.loc['2020-01-01 17:00:00']))
        self.assertEqual(ha_low.loc['2020-01-01 17:01:00'], 0.0)
        self.assertEqual(ha_low.loc['2020-01-01 17:10:00'], 60.0)
        # closing
        ha_closing = feature['ha_closing']
        self.assertTrue(np.isnan(ha_closing.loc['2020-01-01 17:00:00']))
        self.assertEqual(ha_closing.loc['2020-01-01 17:01:00'], 5.0)
        self.assertEqual(ha_closing.loc['2020-01-01 17:10:00'], 65.0)


if __name__ == '__main__':
    unittest.main()