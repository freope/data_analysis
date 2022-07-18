import numpy as np
import pandas as pd

from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyDbmaReverse(StrategyDbma):

    def __init__(
            self,
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            threshold_long=0, threshold_short=0):
        super().__init__(
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            threshold_long, threshold_short)
        
    def convert_open_indicators(self, indicators, position_type):
        # pandas.core.series.Series か numpy.ndarray である必要がある。
        if not (isinstance(indicators, pd.core.series.Series) \
                or isinstance(indicators, np.ndarray)):
            raise ValueError('indicators are invalid type.')

        # 1 次元である必要がある。
        if not len(indicators.shape):
            raise ValueError('should be len(indicators.shape).')

        if position_type == 'long':
            is_rising = indicators < self._threshold_long
            return is_rising
        elif position_type == 'short':
            is_falling = indicators > self._threshold_short
            return is_falling
