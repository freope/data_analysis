import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath('..'))
from frestu.model_selection.split_data_frame import SplitterPercentage


class SplitterPercentageTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1, 10],
                ['2020-01-01 17:01:00', 2, 20],
                ['2020-01-01 17:02:00', 3, 30],
                ['2020-01-01 17:03:00', 4, 40],
                ['2020-01-01 17:04:00', 5, 50],
                ['2020-01-01 17:05:00', 6, 60],
            ],
            columns=['time', 'val_1', 'val_2'],
        ).set_index('time')
    
    def tearDown(self):
        pass
    
    def test_split(self):
        splitter = SplitterPercentage(0.3, 'val_1')
        X_train, y_train, X_test, y_test = splitter.split(self.df)
        self.assertEqual(X_train.shape[0], 2)
        self.assertEqual(y_train.shape[0], 2)
        self.assertEqual(X_test.shape[0], 4)
        self.assertEqual(y_test.shape[0], 4)
        # print(X_train)
        # print(y_train)
        # print(X_test)
        # print(y_test)


if __name__ == '__main__':
    unittest.main()