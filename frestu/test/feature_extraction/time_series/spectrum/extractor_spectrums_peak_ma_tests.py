import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.spectrum import ExtractorSpectrumsPeakMa


class ExtractorSpectrumsPeakMaTests(unittest.TestCase):

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
        windows = range(2, 5)
        self.extractor = ExtractorSpectrumsPeakMa('sma', windows)
    
    def tearDown(self):
        pass
    
    def test_extract(self):
        freqs_peak, spectrum_peak = self.extractor.extract(self.df)
        self.assertEqual(len(spectrum_peak), 3)
        self.assertGreater(spectrum_peak[0], 7.04)
        self.assertLess(spectrum_peak[0], 7.05)
        self.assertGreater(spectrum_peak[2], 11.3)
        self.assertLess(spectrum_peak[2], 11.4)
        # print(freqs_peak)
        # print(spectrum_peak)


if __name__ == '__main__':
    unittest.main()