import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.prediction import ExtractorPrediction
from frestu.feature_extraction.time_series.prediction import PredictorRidge
from frestu.feature_extraction.time_series import ExtractorIdentity
from frestu.feature_selection import SelectorIdentity
from frestu.model_selection.split_data_frame import SplitterNumber


class ExtractorPredictionTests(unittest.TestCase):

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
        self.extractor = ExtractorPrediction(
            extractor, selector, splitter, predictor)
    
    def tearDown(self):
        pass
    
    def test_extract(self):
        y_pred = self.extractor.extract(self.df)
        self.assertGreater(y_pred.iloc[5, 0], 29,1)
        self.assertLess(y_pred.iloc[5, 0], 29.2)
        self.assertGreater(y_pred.iloc[10, 0], 107.8)
        self.assertLess(y_pred.iloc[10, 0], 107.9)
        # print(y_pred)
        # print(extractor_pred.y_test)


if __name__ == '__main__':
    unittest.main()