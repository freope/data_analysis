from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorMa
from frestu.feature_extraction.time_series.spectrum import ExtractorFft


class ExtractorSpectrumMa(ExtractorFeatureAbstract):
    
    def __init__(self, ma_type, window):
        self.__ma_type = ma_type
        self.__window = window
    
    def extract(self, df):
        extractor_ma = ExtractorMa(self.__ma_type, self.__window)

        # SMA 以外の MA にも対応できるよう rolling(window, center=True) を使っていない。
        center = extractor_ma.extract(df)
        center = center.shift(-self.__window // 2)
        
        oscillation = df - center        
        oscillation = oscillation.dropna()
        
        time_span = oscillation.shape[0]
        wave = oscillation.iloc[:, 0]
        
        extractor_fft = ExtractorFft(time_span)
        freqs, spectrum_amp = extractor_fft.extract(wave)
        
        return freqs, spectrum_amp