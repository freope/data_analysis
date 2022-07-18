import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.abspath('..'))
from frestu.model_selection.split_data_frame import SplitterTimeSeriesConstant


class SplitterTimeSeriesConstantTests(unittest.TestCase):

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
    
    def test_split(self):
        splitter = SplitterTimeSeriesConstant(self.df, 3)
        indices_test = [ix_test[0] for ix_train, ix_test in splitter.split()]
        self.assertEqual(len(indices_test), 3)
        self.assertEqual(indices_test[0], '2020-01-01 17:03:00')
        self.assertEqual(indices_test[1], '2020-01-01 17:04:00')
        self.assertEqual(indices_test[2], '2020-01-01 17:05:00')


if __name__ == '__main__':
    unittest.main()    
