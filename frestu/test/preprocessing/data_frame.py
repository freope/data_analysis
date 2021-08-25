import os, sys, unittest
import pandas as pd
from frestu.preprocessing.data_frame import DataFrame


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