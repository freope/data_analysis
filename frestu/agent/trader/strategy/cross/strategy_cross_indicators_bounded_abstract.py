import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract as StrategyParentAbstract


class StrategyCrossIndicatorsBoundedAbstract(StrategyParentAbstract):

    def __init__(
            self,
            bound_long, bound_short,
            threshold_long, threshold_short):
        """
        Notes
        -----
        calculate_closing_times() だけを使う前提の戦略。
        threshold_long, threshold_short ともに 0 であり、
        bound_long, -bound_short が十分大きい場合、
        ドテン売買戦略になるが、そのように使うつもりはない。
        """
        super().__init__()
        self._bound_long = bound_long
        self._bound_short = bound_short
        self._threshold_long = threshold_long
        self._threshold_short = threshold_short
    
    def convert_open_indicators(self, indicators, position_type):
        # pandas.core.series.Series か numpy.ndarray である必要がある。
        if not (isinstance(indicators, pd.core.series.Series) \
                or isinstance(indicators, np.ndarray)):
            raise ValueError('indicators are invalid type.')

        # 1 次元である必要がある。
        if not len(indicators.shape):
            raise ValueError('should be len(indicators.shape).')

        # indicators の 1 行目を NaN にする。
        # indicators[0] = np.nan

        if position_type == 'long':
            is_rising = indicators > self._threshold_long
            is_lower = indicators < self._bound_long
            can_open_long = pd.concat(
                [is_rising, is_lower], axis=1).all(axis=1)
            return can_open_long
        elif position_type == 'short':
            is_falling = indicators < self._threshold_short
            is_higher = indicators > self._bound_short
            can_open_short = pd.concat(
                [is_falling, is_higher], axis=1).all(axis=1)
            return can_open_short