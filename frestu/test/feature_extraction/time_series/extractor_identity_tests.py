import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath('..'))
from frestu.feature_extraction.time_series import ExtractorIdentity


class ExtractorIdentityTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
                ['2020-01-01 17:03:00', 4],
                ['2020-01-01 17:04:00', 5],
                ['2020-01-01 17:05:00', 6],
            ],
            columns=['time', 'val'],
        ).set_index('time')
    
    def tearDown(self):
        pass

    def test_extract(self):
        extractor = ExtractorIdentity()
        feature = extractor.extract(self.df)
        self.assertEqual(feature.iloc[0, 0], self.df.iloc[0, 0])
        self.assertEqual(feature.iloc[1, 0], self.df.iloc[1, 0])
        self.assertEqual(feature.iloc[2, 0], self.df.iloc[2, 0])
        self.assertEqual(feature.iloc[3, 0], self.df.iloc[3, 0])
        self.assertEqual(feature.iloc[4, 0], self.df.iloc[4, 0])
        self.assertEqual(feature.iloc[5, 0], self.df.iloc[5, 0])


if __name__ == '__main__':
    unittest.main()
