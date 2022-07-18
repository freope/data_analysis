import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.spectrum import ExtractorWavelet


class ExtractorWaveletTests(unittest.TestCase):

    def setUp(self):
        self.extractor = ExtractorWavelet(1, 2, 10)
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
        self.assertEqual(len(spectra_amp), 10)
        self.assertEqual(len(spectra_amp[0]), 11)
        self.assertGreater(spectra_amp[0][0], 6.48)
        self.assertLess(spectra_amp[0][0], 6.49)
        self.assertGreater(spectra_amp[0][10], 21.3)
        self.assertLess(spectra_amp[0][10], 21.4)
        self.assertGreater(spectra_amp[9][0], 0.61)
        self.assertLess(spectra_amp[9][0], 0.62)
        self.assertGreater(spectra_amp[9][10], 5.62)
        self.assertLess(spectra_amp[9][10], 5.63)


if __name__ == '__main__':
    unittest.main()