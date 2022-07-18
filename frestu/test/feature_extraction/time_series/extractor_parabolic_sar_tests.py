import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series import ExtractorParabolicSar


class ExtractorParabolicSarTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorParabolicSar()
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
        self.assertEqual(feature.loc['2020-01-01 17:00:00'][0], 0)
        self.assertEqual(feature.loc['2020-01-01 17:06:00'][0], 30)
        self.assertGreater(feature.loc['2020-01-01 17:10:00'][0], 10.9)
        self.assertLess(feature.loc['2020-01-01 17:10:00'][0], 11.0)


if __name__ == '__main__':
    unittest.main()