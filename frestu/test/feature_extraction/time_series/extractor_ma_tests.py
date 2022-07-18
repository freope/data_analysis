import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorMa


class ExtractorMaTests(unittest.TestCase):

    def setUp(self):
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
        self.extractor_sma = ExtractorMa('sma', 2)
        self.extractor_ema = ExtractorMa('ema', 2)
    
    def tearDown(self):
        pass
    
    def test_extract(self):
        # sma
        ma = self.extractor_sma.extract(self.df)
        # ma
        self.assertTrue(np.isnan(ma.loc['2020-01-01 17:00:00'][0]))
        self.assertEqual(ma.loc['2020-01-01 17:01:00'][0], 5)
        self.assertEqual(ma.loc['2020-01-01 17:10:00'][0], 65)

        # ema
        ma = self.extractor_ema.extract(self.df)
        # ma
        self.assertEqual(ma.loc['2020-01-01 17:00:00'][0], 0)
        self.assertGreater(ma.loc['2020-01-01 17:01:00'][0], 6.6)
        self.assertLess(ma.loc['2020-01-01 17:01:00'][0], 6.7)
        self.assertGreater(ma.loc['2020-01-01 17:10:00'][0], 62)
        self.assertLess(ma.loc['2020-01-01 17:10:00'][0], 63)


if __name__ == '__main__':
    unittest.main()