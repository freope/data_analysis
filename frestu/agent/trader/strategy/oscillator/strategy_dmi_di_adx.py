import pandas as pd

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDmi


class StrategyDmiDiAdx(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            window_ohlc, window_tr_dm, window_adx, threshold_adx,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorDmi(window_ohlc, window_tr_dm, window_adx)
        self.__threshold_adx = threshold_adx

    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df)
    
    def convert_open_indicators(self, indicators, position_type):
        di_diff = indicators['+DI'] - indicators['-DI']
        adx = indicators['ADX']
        is_trending = adx > self.__threshold_adx
        if position_type == 'long':
            is_rising = pd.concat(
                [di_diff > self._threshold_long, is_trending],
                axis=1).all(axis=1)
            return is_rising
        elif position_type == 'short':
            is_falling = pd.concat(
                [di_diff < self._threshold_short, is_trending],
                axis=1).all(axis=1)
            return is_falling