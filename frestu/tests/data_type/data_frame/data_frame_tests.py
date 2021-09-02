import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.abspath(".."))
from frestu.data_type.data_frame import DataFrame


class DataFrameTests(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_make_index_unique(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:00:00', 2],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.make_index_unique().shape[0], 1)        
    
    def test_complement_missing_minutes(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:02:00', 3],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        self.assertEqual(df.shape[0], 2)
        self.assertEqual(df.complement_missing_minutes().shape[0], 3)
    
    def test_select_business_minutes(self):
        pass
    
    def test_create_column_log(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        df = df.create_column_log('val')
        for i in range(df.shape[0]):
            self.assertEqual(df['val_log'][i], np.log(df['val'][i]))
    
    def test_create_columns_diff(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        df = df.create_columns_diff('val', [1])
        self.assertTrue(np.isnan(df['val_diff_1'][0]))
        self.assertEqual(df['val_diff_1'][1], 2-1)
        self.assertEqual(df['val_diff_1'][2], 3-2)

    def test_create_columns_past(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        df = df.create_columns_past(
            column='val',
            shifts=range(1,3))
        self.assertEqual(df['val_past_1'][1], 1)
        self.assertEqual(df['val_past_2'][2], 1)
    
    def test_create_columns_future(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 1],
                ['2020-01-01 17:01:00', 2],
                ['2020-01-01 17:02:00', 3],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        df = DataFrame(df)
        df = df.create_columns_future(
            column='val',
            shifts=range(1,3))
        self.assertEqual(df['val_future_1'][1], 3)
        self.assertEqual(df['val_future_2'][0], 3)


if __name__ == '__main__':
    unittest.main()