import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorRaw
from frestu.feature_extraction.time_series.prediction import ExtractorPrediction
from frestu.feature_extraction.time_series.prediction import PredictorRidge
from frestu.feature_extraction.time_series import ExtractorIdentity
from frestu.feature_selection import SelectorIdentity
from frestu.model_selection.split_data_frame import SplitterNumber


class StrategyCrossIndicatorRawTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
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
        extractor = ExtractorIdentity()
        selector = SelectorIdentity()
        splitter = SplitterNumber(5, 'y')
        predictor = PredictorRidge(0.01)
        extractor_pred = ExtractorPrediction(
            extractor, selector, splitter, predictor)
        self.strategy = StrategyCrossIndicatorRaw(extractor_pred, 'y', 'y')
        
    def tearDown(self):
        pass
    
    def test_calculate_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        self.assertTrue(np.isnan(indicator.loc['2020-01-01 17:00:00']))
        self.assertTrue(np.isnan(indicator.loc['2020-01-01 17:04:00']))
        self.assertGreater(indicator.loc['2020-01-01 17:05:00'], -0.87)
        self.assertLess(indicator.loc['2020-01-01 17:05:00'], -0.86)
        self.assertGreater(indicator.loc['2020-01-01 17:10:00'], 17.8)
        self.assertLess(indicator.loc['2020-01-01 17:10:00'], 17.9)
    
    def test_convert_open_indicators(self):
        indicator = self.strategy.calculate_open_indicators(self.df)
        can_open_long = self.strategy.convert_open_indicators(
            indicator, 'long')
        can_open_short = self.strategy.convert_open_indicators(
            indicator, 'short')
        # long
        self.assertFalse(can_open_long['2020-01-01 17:06:00'])
        self.assertTrue(can_open_long['2020-01-01 17:07:00'])
        self.assertFalse(can_open_long['2020-01-01 17:08:00'])
        self.assertTrue(can_open_long['2020-01-01 17:09:00'])
        # short
        self.assertFalse(can_open_short['2020-01-01 17:04:00'])
        self.assertTrue(can_open_short['2020-01-01 17:05:00'])
        self.assertFalse(can_open_short['2020-01-01 17:07:00'])
        self.assertTrue(can_open_short['2020-01-01 17:08:00'])


if __name__ == '__main__':
    unittest.main()