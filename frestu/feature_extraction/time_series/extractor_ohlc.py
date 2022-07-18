import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorOhlc(ExtractorFeatureAbstract):

    def __init__(self, window):
        self.__window = window
    
    def extract(self, df):
        # open price
        o = df.rolling(self.__window).apply(lambda x: x[0])
        # high price
        h = df.rolling(self.__window).max()
        # low price
        l = df.rolling(self.__window).min()
        # closing price
        c = df.rolling(self.__window).apply(lambda x: x[-1])

        ohlc = pd.concat([o, h, l, c], axis=1)
        ohlc.columns = ['open', 'high', 'low', 'closing']

        return ohlc