import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract


class StrategyCrossIndicatorsAbstract(StrategyContinuousIndicatorAbstract):

    def __init__(self, threshold_long, threshold_short):
        """
        Notes
        -----
        threshold_long, threshold_short ともに 0 だった場合、ドテン売買戦略になる。
        """
        super().__init__()
        self._threshold_long = threshold_long
        self._threshold_short = threshold_short
    
    def convert_open_indicators(self, indicators, position_type):
        # NOTE: 以下の 2 点に注意。
        # - indicators は pandas.core.series.Series。
        #   pandas.core.frame.DataFrame ではないことに注意。

        # pandas.core.series.Series。
        if not isinstance(indicators, pd.core.series.Series):
            raise ValueError('indicators are invalid type.')

        # 1 次元である必要がある。
        if not len(indicators.shape):
            raise ValueError('should be len(indicators.shape).')

        if position_type == 'long':
            is_rising = indicators > self._threshold_long
            return is_rising
        elif position_type == 'short':
            is_falling = indicators < self._threshold_short
            return is_falling