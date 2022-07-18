import pandas as pd

from frestu.agent.trader.strategy.period import StrategyRegularIntervalAndSlope
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyRegularIntervalAndCurvature(StrategyRegularIntervalAndSlope):

    def __init__(
            self,
            period_half, offset, ma_type, window,
            window_slope=1, window_curvature=1,
            threshold_long=0, threshold_short=0):
        super().__init__(
            period_half, offset, ma_type, window,
            window_slope, threshold_long, threshold_short)
        self.__window_curvature = window_curvature
    
    def calculate_open_indicators(self, df):
        # indicator regular interval
        slope_ma, indicator_ri = super().calculate_open_indicators(df)

        # 移動平均の曲率の移動平均
        curvature = slope_ma - slope_ma.shift(self.__window_curvature)
        curvature_ma = curvature / self.__window_curvature

        return curvature_ma, indicator_ri
    
    def convert_open_indicators(self, indicators, position_type):
        curvature_ma, indicator_ri = indicators

        if position_type == 'long':
            is_rising = curvature_ma > self._threshold_long
            can_open_long = pd.concat(
                [indicator_ri, is_rising], axis=1).all(axis=1)
            return can_open_long
        elif position_type == 'short':
            indicator_ri = indicator_ri == False
            is_falling = curvature_ma < self._threshold_short
            can_open_short = pd.concat(
                [indicator_ri, is_falling], axis=1).all(axis=1)
            return can_open_short