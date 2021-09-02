import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath(".."))
from frestu.model_selection import train_test_split_time_series


class TrainTestSplitTests(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_train_test_split_time_series(self):
        df = pd.DataFrame(
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
        folds = train_test_split_time_series(df, n_splits=3)
        indices_test = [ix_test[0] for ix_train, ix_test in folds()]
        self.assertEqual(len(indices_test), 3)
        self.assertEqual(indices_test[0], '2020-01-01 17:03:00')
        self.assertEqual(indices_test[1], '2020-01-01 17:04:00')
        self.assertEqual(indices_test[2], '2020-01-01 17:05:00')


if __name__ == '__main__':
    unittest.main()