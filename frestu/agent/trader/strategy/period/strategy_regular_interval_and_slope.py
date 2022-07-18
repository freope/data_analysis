import pandas as pd

from frestu.agent.trader.strategy.period import StrategyRegularInterval
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyRegularIntervalAndSlope(StrategyRegularInterval):

    def __init__(
            self,
            period_half, offset, ma_type, window,
            window_slope=1, threshold_long=0, threshold_short=0):
        super().__init__(period_half, offset)
        self.__extractor_ma = ExtractorMa(ma_type, window)
        self.__window_slope = window_slope
        self._threshold_long = threshold_long
        self._threshold_short = threshold_short
    
    def calculate_open_indicators(self, df):
        # indicator regular interval
        indicator_ri = super().calculate_open_indicators(df)

        # 移動平均
        ma = self.__extractor_ma.extract(df)

        # 移動平均の傾きの移動平均
        slope = ma - ma.shift(self.__window_slope)
        slope_ma = slope / self.__window_slope

        return slope_ma, indicator_ri
    
    def convert_open_indicators(self, indicators, position_type):
        slope_ma, indicator_ri = indicators

        if position_type == 'long':
            is_rising = slope_ma > self._threshold_long
            can_open_long = pd.concat(
                [indicator_ri, is_rising], axis=1).all(axis=1)
            return can_open_long
        elif position_type == 'short':
            indicator_ri = indicator_ri == False
            is_falling = slope_ma < self._threshold_short
            can_open_short = pd.concat(
                [indicator_ri, is_falling], axis=1).all(axis=1)
            return can_open_short