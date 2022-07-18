import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract
from frestu.feature_extraction.time_series import ExtractorOhlc


class ExtractorStochastics(ExtractorFeatureAbstract):

    def __init__(self, x, y, z):
        self.__extractor_ohlc = ExtractorOhlc(x)
        self.__y = y
        self.__z = z
    
    def extract(self, df):
        ohlc = self.__extractor_ohlc.extract(df)

        cl = ohlc['closing'] - ohlc['low']
        hl = ohlc['high'] - ohlc['low']

        p_k = cl / hl
        p_d = cl.rolling(self.__y).sum() / hl.rolling(self.__y).sum()
        slow_p_d = p_d.rolling(self.__z).mean()

        stochastics = pd.concat([p_k, p_d, slow_p_d], axis=1)
        stochastics.columns = ['%K', '%D', 'Slow%D']

        return stochastics