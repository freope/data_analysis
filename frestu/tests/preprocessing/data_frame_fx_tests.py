import os
import sys
import unittest
sys.path.append(os.path.abspath(".."))
from frestu.preprocessing.data_frame import DataFrameFx


class DataFrameFxTests(unittest.TestCase):
    def setUp(self):
        self.df = DataFrameFx([0, 10, 5, 3, 8], columns=['rate'])

    def tearDown(self):
        pass

    def test_max_profit(self):
        profit = self.df.max_profit('rate')
        self.assertEqual(profit, 15)
    
    def test_max_loss(self):
        loss = self.df.max_loss('rate')
        self.assertEqual(loss, -7)


if __name__ == '__main__':
    unittest.main()