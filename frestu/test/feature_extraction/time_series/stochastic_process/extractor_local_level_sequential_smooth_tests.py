import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.stochastic_process import ExtractorLocalLevelSequentialSmooth


class ExtractorLocalLevelSequentialSmoothTests(unittest.TestCase):

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
        self.extractor = ExtractorLocalLevelSequentialSmooth(
            'val', 1, 0, 10000000, 1000, 10000, True, True)

    def tearDown(self):
        pass
    
    def test_extract(self):
        feature = self.extractor.extract(self.df)
        # mu_sequential_smooth
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'mu_sequential_smooth'], -0.1)
        self.assertLess(
            feature.loc['2020-01-01 17:00:00', 'mu_sequential_smooth'], 0.1)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'mu_sequential_smooth'], 37.3)
        self.assertLess(
            feature.loc['2020-01-01 17:10:00', 'mu_sequential_smooth'], 37.4)
        # sigma_sequential_smooth
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'sigma_sequential_smooth'],
            104.8)
        self.assertLess(
            feature.loc['2020-01-01 17:00:00', 'sigma_sequential_smooth'],
            104.9)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'sigma_sequential_smooth'], 46.6)
        self.assertLess(
            feature.loc['2020-01-01 17:10:00', 'sigma_sequential_smooth'], 46.7)
        # mu_filter
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'mu_filter'], -0.1)
        self.assertLess(feature.loc['2020-01-01 17:00:00', 'mu_filter'], 0.1)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'mu_filter'], 40.3)
        self.assertLess(feature.loc['2020-01-01 17:10:00', 'mu_filter'], 40.4)
        # sigma_filter
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'sigma_filter'], 3162.4)
        self.assertLess(
            feature.loc['2020-01-01 17:00:00', 'sigma_filter'], 3162.5)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'sigma_filter'], 60.9)
        self.assertLess(
            feature.loc['2020-01-01 17:10:00', 'sigma_filter'], 70.0)
        # mu_smooth
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'mu_smooth'], 14.9)
        self.assertLess(feature.loc['2020-01-01 17:00:00', 'mu_smooth'], 15.0)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'mu_smooth'], 40.3)
        self.assertLess(feature.loc['2020-01-01 17:10:00', 'mu_smooth'], 40.4)
        # sigma_smooth
        self.assertGreater(
            feature.loc['2020-01-01 17:00:00', 'sigma_smooth'], 52.0)
        self.assertLess(
            feature.loc['2020-01-01 17:00:00', 'sigma_smooth'], 52.1)
        self.assertGreater(
            feature.loc['2020-01-01 17:10:00', 'sigma_smooth'], 52.0)
        self.assertLess(
            feature.loc['2020-01-01 17:10:00', 'sigma_smooth'], 52.1)


if __name__ == '__main__':
    unittest.main()