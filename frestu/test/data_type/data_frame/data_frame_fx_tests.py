import os
import sys
import unittest

sys.path.append(os.path.abspath('..'))
from frestu.data_type.data_frame import DataFrameFx


class DataFrameFxTests(unittest.TestCase):

    def setUp(self):
        self.df = DataFrameFx([0, 10, 5, 3, 8], columns=['rate'])

    def tearDown(self):
        pass

    def test_sum_rising(self):
        rising = self.df.sum_rising('rate')
        self.assertEqual(rising, 15)
    
    def test_sum_falling(self):
        falling = self.df.sum_falling('rate')
        self.assertEqual(falling, -7)

    def test_sum_changing(self):
        changing = self.df.sum_changing('rate')
        self.assertEqual(changing, 22)

    def test_select_business_minutes(self):
        pass


if __name__ == '__main__':
    unittest.main()