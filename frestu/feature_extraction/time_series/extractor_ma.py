import pandas as pd

from frestu.feature_extraction import ExtractorFeatureAbstract


class ExtractorMa(ExtractorFeatureAbstract):

    def __init__(self, ma_type, window):
        self.__ma_type = ma_type
        self.__window = window
    
    def extract(self, df):
        if self.__ma_type == 'sma':
            rolling = df.rolling(self.__window)
            ma = rolling.mean()
            return ma
        elif self.__ma_type == 'ema':
            rolling = df.ewm(span=self.__window, adjust=False)
            ma = rolling.mean()
            return ma