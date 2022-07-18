import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.spectrum import ExtractorFft


class ExtractorFftTests(unittest.TestCase):

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
        self.extractor = ExtractorFft(11)

    def tearDown(self):
        pass

    def test_extract(self):
        wave = self.df.iloc[:, 0]
        freqs, spectrum_amp = self.extractor.extract(wave)
        self.assertEqual(len(spectrum_amp), 4)
        self.assertGreater(spectrum_amp[0], 14)
        self.assertLess(spectrum_amp[0], 15)
        self.assertGreater(spectrum_amp[3], 8)
        self.assertLess(spectrum_amp[3], 9)


if __name__ == '__main__':
    unittest.main()