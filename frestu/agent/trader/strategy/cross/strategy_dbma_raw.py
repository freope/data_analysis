import pandas as pd

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDbma
from frestu.feature_extraction.time_series import ExtractorDfma


class StrategyDbmaRaw(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_dfma = ExtractorDfma(ma_type_shorter, window_shorter)
        self.__extractor_dbma = ExtractorDbma(
            ma_type_shorter, window_shorter, ma_type_longer, window_longer)
    
    def calculate_open_indicators(self, df):
        dfma = self.__extractor_dfma.extract(df)
        dbma = self.__extractor_dbma.extract(df)
        return {'dfma': dfma, 'dbma': dbma}
    
    def convert_open_indicators(self, indicators, position_type):
        if position_type == 'long':
            is_rising_dfma = indicators['dfma'] > 0
            is_rising_dbma = indicators['dbma'] > self._threshold_long
            is_rising = pd.concat(
                [is_rising_dfma, is_rising_dbma], axis=1).all(axis=1)
            return is_rising
        elif position_type == 'short':
            is_falling_dfma = indicators['dfma'] < 0
            is_falling_dbma = indicators['dbma'] < self._threshold_short
            is_falling = pd.concat(
                [is_falling_dfma, is_falling_dbma], axis=1).all(axis=1)
            return is_falling
