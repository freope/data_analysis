import os, sys, unittest
from frestu.preprocessing.data_frame_frestu_fx import DataFrameFrestuFx


class DataFrameFrestuFxTests(unittest.TestCase):
    def setUp(self):
        self.df = DataFrameFrestuFx([0, 10, 5, 3, 8], columns=['rate'])

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