import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath('..'))
from frestu.feature_selection import SelectorIdentity


class SelectorIdentityTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
                ['2020-01-01 17:03:00', 4],
                ['2020-01-01 17:04:00', 5],
            ],
            columns=['time', 'val'],
        ).set_index('time')
    
    def tearDown(self):
        pass
    
    def test_select(self):
        selector = SelectorIdentity()
        feature = selector.select(self.df)
        self.assertEqual(feature.iloc[0, 0], self.df.iloc[0, 0])
        self.assertEqual(feature.iloc[1, 0], self.df.iloc[1, 0])
        self.assertEqual(feature.iloc[2, 0], self.df.iloc[2, 0])
        self.assertEqual(feature.iloc[3, 0], self.df.iloc[3, 0])
        self.assertEqual(feature.iloc[4, 0], self.df.iloc[4, 0])


if __name__ == '__main__':
    unittest.main()