import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.regression import StrategyCrossRidgeRaw
from frestu.data_type.data_frame import DataFrame


class StrategyCrossRidgeRawTests(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 0, 10],
                ['2020-01-01 17:01:00', 10, 20],
                ['2020-01-01 17:02:00', 20, 40],
                ['2020-01-01 17:03:00', 30, 60],
                ['2020-01-01 17:04:00', 25, 30],
                ['2020-01-01 17:05:00', 15, 30],
                ['2020-01-01 17:06:00', 5, 50],
                ['2020-01-01 17:07:00', 10, 20],
                ['2020-01-01 17:08:00', 30, 80],
                ['2020-01-01 17:09:00', 60, 70],
                ['2020-01-01 17:10:00', 70, 90],
            ],
            columns=['time', 'X', 'y'],
        ).set_index('time')
        self.df = DataFrame(df).add_cols_past(
            columns=['X'],
            shifts=range(1, 3)
        ).dropna()
        self.strategy = StrategyCrossRidgeRaw.create(
            future_shift=1, zerones=[1, 0, 1], n_data_train=5,
            col_indicator='future', col_raw='y', can_fit=True, alpha=0.01)

    def tearDown(self):
        pass
    
    def test_calculate_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        self.assertTrue(np.isnan(indicator.loc['2020-01-01 17:06:00']))
        self.assertGreater(indicator.loc['2020-01-01 17:07:00'], 30.2)
        self.assertLess(indicator.loc['2020-01-01 17:07:00'], 30.3)
        self.assertGreater(indicator.loc['2020-01-01 17:10:00'], -78.9)
        self.assertLess(indicator.loc['2020-01-01 17:10:00'], -78.8)

    def test_convert_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:06:00'])
        self.assertTrue(can_open_long['2020-01-01 17:07:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:07:00'])
        self.assertTrue(can_open_short['2020-01-01 17:08:00'])


if __name__ == '__main__':
    unittest.main()