import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorDfma


class ExtractorDfmaTests(unittest.TestCase):

    def setUp(self):
        self.extractor_dfsma = ExtractorDfma('sma', 2)
        self.extractor_dfema = ExtractorDfma('ema', 2)
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
        # dfsma
        feature = self.extractor_dfsma.extract(self.df)
        self.assertTrue(np.isnan(feature.loc['2020-01-01 17:00:00'][0]))
        self.assertEqual(feature.loc['2020-01-01 17:01:00'][0], 5)
        self.assertEqual(feature.loc['2020-01-01 17:09:00'][0], 15)
        # dfema
        feature = self.extractor_dfema.extract(self.df)
        self.assertEqual(feature.loc['2020-01-01 17:00:00'][0], 0)
        self.assertGreater(feature.loc['2020-01-01 17:01:00'][0], 3.3)
        self.assertLess(feature.loc['2020-01-01 17:01:00'][0], 3.4)
        self.assertGreater(feature.loc['2020-01-01 17:10:00'][0], 7.4)
        self.assertLess(feature.loc['2020-01-01 17:10:00'][0], 7.5)


if __name__ == '__main__':
    unittest.main()