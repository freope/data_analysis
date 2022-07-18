import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath('..'))
from frestu.feature_selection import SelectorWhiteColumns


class SelectorWhiteColumnsTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1, 6, 'a'],
                ['2020-01-01 17:01:00', 2, 7, 'b'],
                ['2020-01-01 17:02:00', 3, 8, 'c'],
                ['2020-01-01 17:03:00', 4, 9, 'd'],
                ['2020-01-01 17:04:00', 5, 0, 'e'],
            ],
            columns=['time', 'val_1', 'val_2', 'val_3'],
        ).set_index('time')
    
    def tearDown(self):
        pass
    
    def test_select(self):
        selector = SelectorWhiteColumns([0, 2])
        feature = selector.select(self.df)
        # 0 列目
        self.assertEqual(feature.iloc[0, 0], self.df.iloc[0, 0])
        self.assertEqual(feature.iloc[1, 0], self.df.iloc[1, 0])
        self.assertEqual(feature.iloc[2, 0], self.df.iloc[2, 0])
        self.assertEqual(feature.iloc[3, 0], self.df.iloc[3, 0])
        self.assertEqual(feature.iloc[4, 0], self.df.iloc[4, 0])
        # 1 列目
        self.assertEqual(feature.iloc[0, 1], self.df.iloc[0, 2])
        self.assertEqual(feature.iloc[1, 1], self.df.iloc[1, 2])
        self.assertEqual(feature.iloc[2, 1], self.df.iloc[2, 2])
        self.assertEqual(feature.iloc[3, 1], self.df.iloc[3, 2])
        self.assertEqual(feature.iloc[4, 1], self.df.iloc[4, 2])


if __name__ == '__main__':
    unittest.main()