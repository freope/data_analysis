import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorStochastics


class ExtractorStochasticsTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorStochastics(2, 2, 2)
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
        p_k = indicators['%K']
        p_d = indicators['%D']
        slow_p_d = indicators['Slow%D']
        # %K
        self.assertTrue(np.isnan(p_k.loc['2020-01-01 17:00:00']))
        self.assertEqual(p_k.loc['2020-01-01 17:01:00'], 1)
        self.assertEqual(p_k.loc['2020-01-01 17:06:00'], 0)
        # %D
        self.assertTrue(np.isnan(p_d.loc['2020-01-01 17:00:00']))
        self.assertEqual(p_d.loc['2020-01-01 17:02:00'], 1)
        self.assertGreater(p_d.loc['2020-01-01 17:07:00'], 0.33)
        self.assertLess(p_d.loc['2020-01-01 17:07:00'], 0.34)
        # Slow%D
        self.assertTrue(np.isnan(slow_p_d.loc['2020-01-01 17:00:00']))
        self.assertEqual(slow_p_d.loc['2020-01-01 17:03:00'], 1)
        self.assertGreater(slow_p_d.loc['2020-01-01 17:07:00'], 0.16)
        self.assertLess(slow_p_d.loc['2020-01-01 17:07:00'], 0.17)


if __name__ == '__main__':
    unittest.main()