import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.prediction import BuilderFeature
from frestu.feature_extraction.time_series.prediction import ExtractorPredictionIterable
from frestu.feature_extraction.time_series.prediction import PredictorRidge
from frestu.feature_extraction.time_series import ExtractorIdentity
from frestu.feature_selection import SelectorIdentity
from frestu.model_selection.split_data_frame import SplitterNumber



class Builder(BuilderFeature):
    
    def _make_features_internal(self, df):
        features = pd.concat([df, df * 2], axis=1)
        return features

    def _make_features_external(self, df):
        features = pd.concat([df, df + 2], axis=1)
        return features

    def _make_features_mixed(self, df_i, df_e):
        features_i = self._make_features_internal(df_i)
        features_e = self._make_features_external(df_e)
        features_mixed = features_i.iloc[:, 0] + features_e.iloc[:, 0]
        features_mixed = features_mixed.to_frame()
        return features_mixed

class ExtractorPredictionIterableTests(unittest.TestCase):

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
        df_internal = df[['y']]
        df_external = pd.concat([df[['X']], df[['X']] + 1], axis=1)
        df_external_pred = df_external.shift(-2).fillna(method='ffill') + 1
        extractor = ExtractorIdentity()
        selector = SelectorIdentity()
        splitter_train = SplitterNumber(2, 0)
        splitter_test = SplitterNumber(0, 0)
        predictor = PredictorRidge(0.01)
        builder = Builder(
            2,
            [range(2), range(0, 6, 2)],
            [range(2) for _ in range(4)],
            [range(3)])
        builder.build(df_internal, df_external)
        self.df = builder.features
        self.extractor = ExtractorPredictionIterable(
            extractor, selector, splitter_train, splitter_test, predictor,
            builder, 2,
            df_external_pred)
    
    def tearDown(self):
        pass

    def test_extract(self):
        y_pred = self.extractor.extract(self.df.iloc[4:9])
        # print(y_pred)
        self.assertTrue(np.isnan(y_pred.iloc[0, 0]))
        self.assertTrue(np.isnan(y_pred.iloc[1, 0]))
        self.assertEqual(y_pred.iloc[2, 0], 30)
        self.assertEqual(y_pred.iloc[3, 0], 30)
        self.assertEqual(y_pred.iloc[4, 0], 30)


if __name__ == '__main__':
    unittest.main()