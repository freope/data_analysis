from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series.spectrum import ExtractorSpectrumMa


class ExtractorSpectrumsPeakMa(ExtractorFeatureAbstract):
    
    def __init__(self, ma_type, windows):
        self.__ma_type = ma_type
        self.__windows = windows
    
    def extract(self, df):
        freqs_peak = []
        spectrum_peak = []

        for window in self.__windows:
            extractor = ExtractorSpectrumMa(self.__ma_type, window)
            
            freqs, spectrum_amp = extractor.extract(df)

            ix = spectrum_amp.argmax()
            freq = freqs[ix]
            spectra = spectrum_amp[ix]

            freqs_peak.append(freq)
            spectrum_peak.append(spectra)
        
        return freqs_peak, spectrum_peak