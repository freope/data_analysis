import pandas as pd

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorMa
from frestu.feature_extraction.time_series import ExtractorMstd


class StrategyBbCrossMaSigma(StrategyCrossIndicatorsAbstract):

    def __init__(
            self, ma_type, window, ma_type_bb, window_bb, sigma_coeff,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_ma = ExtractorMa(ma_type, window)
        self.__extractor_ma_bb = ExtractorMa(ma_type_bb, window_bb)
        self.__extractor_mstd_bb = ExtractorMstd(ma_type_bb, window_bb)
        self.__sigma_coeff = sigma_coeff
    
    def calculate_open_indicators(self, df):
        ma = self.__extractor_ma.extract(df)
        ma_bb = self.__extractor_ma_bb.extract(df)
        sigma = self.__extractor_mstd_bb.extract(df)

        indicator_long = ma - (ma_bb + self.__sigma_coeff * sigma)
        indicator_short = ma - (ma_bb - self.__sigma_coeff * sigma)

        indicator_long = indicator_long.iloc[:, 0]
        indicator_short = indicator_short.iloc[:, 0]

        return indicator_long, indicator_short

    def convert_open_indicators(self, indicators, position_type):
        indicator_long, indicator_short = indicators

        if position_type == 'long':
            is_rising = indicator_long > self._threshold_long
            return is_rising
        elif position_type == 'short':
            is_falling = indicator_short < self._threshold_short
            return is_falling