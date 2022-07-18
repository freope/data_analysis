import os
import sys
import unittest

import numpy as np
import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.prediction import BuilderFeature


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


class BuilderFeatureTests(unittest.TestCase):

    def setUp(self):
        df = pd.DataFrame(
            [
                ['2020-01-01 17:00:00', 0],
                ['2020-01-01 17:01:00', 10],
                ['2020-01-01 17:02:00', 20],
                ['2020-01-01 17:03:00', 30],
                ['2020-01-01 17:04:00', 25],
                ['2020-01-01 17:05:00', 15],
                ['2020-01-01 17:06:00', 5],
                ['2020-01-01 17:07:00', 10],
                ['2020-01-01 17:08:00', 30],
                ['2020-01-01 17:09:00', 60],
                ['2020-01-01 17:10:00', 70],
            ],
            columns=['time', 'val'],
        ).set_index('time')
        self.df_internal = df.copy()
        self.df_external = pd.concat([df, df + 1], axis=1)
        self.df_internal_pred = self.df_internal.shift(-2).fillna(
            method='ffill') + 1
        self.df_external_pred = self.df_external.shift(-2).fillna(
            method='ffill') + 1
        self.builder = Builder(
            2,
            [range(2), range(0, 6, 2)],
            [range(2) for _ in range(4)],
            [range(3)])

    def tearDwon(self):
        pass
    
    def test_build(self):
        self.builder.build(self.df_internal, self.df_external)
        features = self.builder.features
        
        # 2020-01-01 17:00:00
        self.assertEqual(features.iloc[0, 0], 0)
        self.assertTrue(np.isnan(features.iloc[0, 1]))
        self.assertEqual(features.iloc[0, 2], 0)
        self.assertTrue(np.isnan(features.iloc[0, 3]))
        self.assertTrue(np.isnan(features.iloc[0, 4]))
        self.assertEqual(features.iloc[0, 5], 0)
        self.assertTrue(np.isnan(features.iloc[0, 6]))
        self.assertEqual(features.iloc[0, 7], 1)
        self.assertTrue(np.isnan(features.iloc[0, 8]))
        self.assertEqual(features.iloc[0, 9], 2)
        self.assertTrue(np.isnan(features.iloc[0, 10]))
        self.assertEqual(features.iloc[0,11], 3)
        self.assertTrue(np.isnan(features.iloc[0, 12]))
        self.assertEqual(features.iloc[0,13], 0)
        self.assertTrue(np.isnan(features.iloc[0, 14]))
        self.assertTrue(np.isnan(features.iloc[0, 15]))

        # 2020-01-01 17:05:00
        self.assertEqual(features.iloc[5, 0], 15)
        self.assertEqual(features.iloc[5, 1], 25)
        self.assertEqual(features.iloc[5, 2], 30)
        self.assertEqual(features.iloc[5, 3], 60)
        self.assertEqual(features.iloc[5, 4], 20)
        self.assertEqual(features.iloc[5, 5], 15)
        self.assertEqual(features.iloc[5, 6], 25)
        self.assertEqual(features.iloc[5, 7], 16)
        self.assertEqual(features.iloc[5, 8], 26)
        self.assertEqual(features.iloc[5, 9], 17)
        self.assertEqual(features.iloc[5, 10], 27)
        self.assertEqual(features.iloc[5, 11], 18)
        self.assertEqual(features.iloc[5, 12], 28)
        self.assertEqual(features.iloc[5, 13], 30)
        self.assertEqual(features.iloc[5, 14], 50)
        self.assertEqual(features.iloc[5, 15], 60)
        
        # 2020-01-01 17:10:00
        self.assertEqual(features.iloc[10, 0], 70)
        self.assertEqual(features.iloc[10, 1], 60)
        self.assertEqual(features.iloc[10, 2], 140)
        self.assertEqual(features.iloc[10, 3], 60)
        self.assertEqual(features.iloc[10, 4], 10)
        self.assertEqual(features.iloc[10, 5], 70)
        self.assertEqual(features.iloc[10, 6], 60)
        self.assertEqual(features.iloc[10, 7], 71)
        self.assertEqual(features.iloc[10, 8], 61)
        self.assertEqual(features.iloc[10, 9], 72)
        self.assertEqual(features.iloc[10, 10], 62)
        self.assertEqual(features.iloc[10, 11], 73)
        self.assertEqual(features.iloc[10, 12], 63)
        self.assertEqual(features.iloc[10, 13], 140)
        self.assertEqual(features.iloc[10, 14], 120)
        self.assertEqual(features.iloc[10, 15], 60)

    
    def test_rebuild(self):
        self.builder.build(self.df_internal, self.df_external)
        # print(self.builder.features)

        self.builder.rebuild(self.df_internal_pred, self.df_external_pred)
        # print(self.builder.features)

        features = self.builder.features

        # 2020-01-01 17:00:00
        self.assertEqual(features.iloc[0, 0], 21)
        self.assertTrue(np.isnan(features.iloc[0, 1]))
        self.assertEqual(features.iloc[0, 2], 42)
        self.assertEqual(features.iloc[0, 3], 0)
        self.assertTrue(np.isnan(features.iloc[0, 4]))
        self.assertEqual(features.iloc[0, 5], 21)
        self.assertTrue(np.isnan(features.iloc[0, 6]))
        self.assertEqual(features.iloc[0, 7], 22)
        self.assertTrue(np.isnan(features.iloc[0, 8]))
        self.assertEqual(features.iloc[0, 9], 23)
        self.assertTrue(np.isnan(features.iloc[0, 10]))
        self.assertEqual(features.iloc[0, 11], 24)
        self.assertTrue(np.isnan(features.iloc[0, 12]))
        self.assertEqual(features.iloc[0, 13], 42)
        self.assertTrue(np.isnan(features.iloc[0, 14]))
        self.assertEqual(features.iloc[0, 15], 0)

        # 2020-01-01 17:05:00
        self.assertEqual(features.iloc[5, 0], 11)
        self.assertEqual(features.iloc[5, 1], 6)
        self.assertEqual(features.iloc[5, 2], 22)
        self.assertEqual(features.iloc[5, 3], 30)
        self.assertEqual(features.iloc[5, 4], 60)
        self.assertEqual(features.iloc[5, 5], 11)
        self.assertEqual(features.iloc[5, 6], 6)
        self.assertEqual(features.iloc[5, 7], 12)
        self.assertEqual(features.iloc[5, 8], 7)
        self.assertEqual(features.iloc[5, 9], 13)
        self.assertEqual(features.iloc[5, 10], 8)
        self.assertEqual(features.iloc[5, 11], 14)
        self.assertEqual(features.iloc[5, 12], 9)
        self.assertEqual(features.iloc[5, 13], 22)
        self.assertEqual(features.iloc[5, 14], 12)
        self.assertEqual(features.iloc[5, 15], 30)

        # 2020-01-01 17:10:00
        self.assertEqual(features.iloc[10, 0], 71)
        self.assertEqual(features.iloc[10, 1], 71)
        self.assertEqual(features.iloc[10, 2], 142)
        self.assertEqual(features.iloc[10, 3], 140)
        self.assertEqual(features.iloc[10, 4], 60)
        self.assertEqual(features.iloc[10, 5], 71)
        self.assertEqual(features.iloc[10, 6], 71)
        self.assertEqual(features.iloc[10, 7], 72)
        self.assertEqual(features.iloc[10, 8], 72)
        self.assertEqual(features.iloc[10, 9], 73)
        self.assertEqual(features.iloc[10, 10], 73)
        self.assertEqual(features.iloc[10, 11], 74)
        self.assertEqual(features.iloc[10, 12], 74)
        self.assertEqual(features.iloc[10, 13], 142)
        self.assertEqual(features.iloc[10, 14], 142)
        self.assertEqual(features.iloc[10, 15], 140)


if __name__ == '__main__':
    unittest.main()