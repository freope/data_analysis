import os
import sys
import unittest

import pandas as pd

sys.path.append(os.path.join('..'))
from frestu.feature_extraction.time_series.spectrum import ExtractorSpectrumMa


class ExtractorSpectrumMaTests(unittest.TestCase):

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
        self.extractor = ExtractorSpectrumMa('sma', 4)
    
    def tearDown(self):
        pass
    
    def test_extract(self):
        freqs, spectrum_amp = self.extractor.extract(self.df)
        self.assertEqual(len(spectrum_amp), 3)
        self.assertGreater(spectrum_amp[0], 11.3)
        self.assertLess(spectrum_amp[0], 11.4)
        self.assertGreater(spectrum_amp[2], 1.09)
        self.assertLess(spectrum_amp[2], 1.10)
        # print(freqs)
        # print(spectrum_amp)


if __name__ == '__main__':
    unittest.main()