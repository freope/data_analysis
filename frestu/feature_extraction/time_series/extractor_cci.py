from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorOhlc


class ExtractorCci(ExtractorFeatureAbstract):

    def __init__(self, window, window_ohlc):
        self.__window = window
        self.__extractor_ohlc = ExtractorOhlc(window_ohlc)

    def extract(self, df):
        ohlc = self.__extractor_ohlc.extract(df)
        tp = (ohlc['high'] + ohlc['low'] + ohlc['closing']) / 3
        ma = tp.rolling(self.__window).mean()
        md = (tp - ma).abs().rolling(self.__window).mean()
        cci = (tp - ma) / (0.015 * md)
        return cci