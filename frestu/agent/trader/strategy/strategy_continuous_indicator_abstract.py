import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyIndependentCloseAbstract


class StrategyContinuousIndicatorAbstract(StrategyIndependentCloseAbstract):
    """
    時間的に連続して現れるような指標に対応させたクラス。

    Notes
    -----
    以下の 2 つの関係が成立する。
    
    * calculate_open_indicators と calculate_close_indicators の出力が同じ。
    * convert_open_indicators と convert_close_indicators の出力が逆。

    これにより、open した position をいつ close させるのかを簡単に求めることが
    できるようになり、StrategyIndependentCloseAbstract クラスの 2 つのメソッド

    * calculate_closing_times

    が持つ以下の性質

    * xxx_opening_times と can_close_xxx が対応したキュー構造。

    を少ない計算コストで満たすことができるようになる。
    """

    def __init__(self):
        super().__init__(indicators_are_corresponded=True)

    def calculate_times(self, df):
        """
        Notes
        -----
        StrategyIndependentCloseAbstract の同メソッドも使用可能だが、
        計算量削減のために opening_times 導出から再実装している。
        """
        # open
        open_indicators = self.calculate_open_indicators(df)

        # long open
        is_rising = self.convert_open_indicators(
            open_indicators, position_type='long')        
        opening_times_long = self._specify_opening_times(is_rising)

        # short open
        is_falling = self.convert_open_indicators(
            open_indicators, position_type='short')
        opening_times_short = self._specify_opening_times(is_falling)

        # NOTE: 計算量削減のため
        # calculate_close_indicators, convert_close_indicators
        # を呼び出さずに、直接計算している。
        is_not_rising = ~is_rising
        is_not_falling = ~is_falling

        # long closed
        closing_times_long = self._specify_closing_times(is_not_rising)

        # short closed
        closing_times_short = self._specify_closing_times(is_not_falling)

        opening_times = opening_times_long, opening_times_short
        closing_times = closing_times_long, closing_times_short

        return opening_times, closing_times

    def calculate_close_indicators(self, df):
        return self.calculate_open_indicators(df)

    def convert_close_indicators(self, indicators, position_type):
        return ~self.convert_open_indicators(indicators, position_type)

    def _specify_closing_times(self, is_not_trending):
        if is_not_trending.shape[0] == 0:
            return []
        return self._specify_trade_times(is_not_trending)