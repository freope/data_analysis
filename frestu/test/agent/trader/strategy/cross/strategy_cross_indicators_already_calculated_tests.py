import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAlreadyCalculated
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyCrossIndicatorsAlreadyCalculatedTests(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame(
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
        extractor = ExtractorMa('sma', 2)
        indicators = extractor.extract(self.df)
        self.strategy = StrategyCrossIndicatorsAlreadyCalculated(indicators)

    def tearDown(self):
        pass

    def test_calculate_open_indicators(self):
        df = self.df.loc['2020-01-01 17:05:00':'2020-01-01 17:10:00', :]
        indicator = self.strategy.calculate_open_indicators(df)
        self.assertEqual(indicator.shape[0], 6)
        self.assertEqual(indicator.loc['2020-01-01 17:05:00'], 20)
        self.assertEqual(indicator.loc['2020-01-01 17:10:00'], 65)
        # print(indicator)


if __name__ == '__main__':
    unittest.main()