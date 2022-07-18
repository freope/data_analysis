import pandas as pd

from frestu.agent.trader.strategy.trend import StrategyRainbow
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyRainbowLimitingSlope(StrategyRainbow):
    
    def __init__(
            self,
            ma_type,
            window_shorter, window_medium, window_longer,
            threshold_slope_long=0, threshold_slope_short=0):
        super().__init__(ma_type, window_shorter, window_medium, window_longer)
        self.__threshold_slope_long = threshold_slope_long
        self.__threshold_slope_short = threshold_slope_short
    
    def calculate_open_indicators(self, df):
        indicator = super().calculate_open_indicators(df)

        ma_longer = self._extractor_longer.extract(df)
        slope_longer = ma_longer - ma_longer.shift(1)

        # long
        condition_parent_long = super().convert_open_indicators(
            indicator, position_type='long')
        condition_slope_long = slope_longer > self.__threshold_slope_long
        can_open_long = [
            condition_parent_long,
            condition_slope_long,
        ]
        can_open_long = pd.concat(can_open_long, axis=1).all(axis=1)

        # short
        condition_parent_short = super().convert_open_indicators(
            indicator, position_type='short')
        condition_slope_short = slope_longer < self.__threshold_slope_short
        can_open_short = [
            condition_parent_short,
            condition_slope_short,
        ]
        can_open_short = pd.concat(can_open_short, axis=1).all(axis=1)

        can_open = pd.concat([can_open_long, can_open_short], axis=1)
        can_open.columns = ['long', 'short']
        
        return can_open