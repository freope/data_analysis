import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorMstd


class ExtractorMstdTests(unittest.TestCase):

    def setUp(self):
        self.extractor_sma = ExtractorMstd('sma', 2)
        self.extractor_ema = ExtractorMstd('ema', 2)
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
        # sma
        sigma = self.extractor_sma.extract(self.df)
        # sigma
        self.assertTrue(np.isnan(sigma.loc['2020-01-01 17:00:00'][0]))
        self.assertGreater(sigma.loc['2020-01-01 17:01:00'][0], 7.0)
        self.assertLess(sigma.loc['2020-01-01 17:01:00'][0], 7.1)
        self.assertGreater(sigma.loc['2020-01-01 17:09:00'][0], 21)
        self.assertLess(sigma.loc['2020-01-01 17:09:00'][0], 22)

        # ema
        sigma = self.extractor_ema.extract(self.df)
        # sigma
        self.assertTrue(np.isnan(sigma.loc['2020-01-01 17:00:00'][0]))
        self.assertGreater(sigma.loc['2020-01-01 17:01:00'][0], 7.0)
        self.assertLess(sigma.loc['2020-01-01 17:01:00'][0], 7.1)
        self.assertGreater(sigma.loc['2020-01-01 17:09:00'][0], 25)
        self.assertLess(sigma.loc['2020-01-01 17:09:00'][0], 26)


if __name__ == '__main__':
    unittest.main()