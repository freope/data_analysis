import pandas as pd

from frestu.agent.trader.strategy.period import StrategyRegularIntervalAndSlope
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyRegularIntervalAndReverseSlope(StrategyRegularIntervalAndSlope):
    
    def convert_open_indicators(self, indicators, position_type):
        slope_ma, indicator_ri = indicators

        if position_type == 'long':
            is_rising = slope_ma < self._threshold_long
            can_open_long = pd.concat(
                [indicator_ri, is_rising], axis=1).all(axis=1)
            return can_open_long
        elif position_type == 'short':
            indicator_ri = indicator_ri == False
            is_falling = slope_ma > self._threshold_short
            can_open_short = pd.concat(
                [indicator_ri, is_falling], axis=1).all(axis=1)
            return can_open_short