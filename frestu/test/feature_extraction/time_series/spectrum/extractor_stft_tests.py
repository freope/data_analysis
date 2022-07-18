import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.spectrum import ExtractorStft


class ExtractorStftTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorStft(11, 6, 1)
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

    def tearDown(self):
        pass

    def test_extract(self):
        wave = self.df.iloc[:, 0]
        freqs, spectra_amp = self.extractor.extract(wave)
        self.assertEqual(len(spectra_amp), 6)
        self.assertGreater(spectra_amp[0][0], 13)
        self.assertLess(spectra_amp[0][0], 14)
        self.assertGreater(spectra_amp[0][1], 1.6)
        self.assertLess(spectra_amp[0][1], 1.7)
        self.assertGreater(spectra_amp[5][0], 33.4)
        self.assertLess(spectra_amp[5][0], 33.5)
        self.assertGreater(spectra_amp[5][1], 10.1)
        self.assertLess(spectra_amp[5][1], 10.2)


if __name__ == '__main__':
    unittest.main()