import pyximport
pyximport.install()

from datetime import datetime as dt

import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyComponentAbstract
from frestu.agent.trader.strategy.strategy_independent_close.convert_with_cython import convert_with_cython


class StrategyIndependentCloseAbstract(StrategyComponentAbstract):
    """
    Notes
    -----
    opening_times と closing_times が独立に計算できる戦略の抽象クラス。
    さらに、opening_times と closing_times を独立に計算できる戦略は、
    以下の 2 つに分かれる。
    * opening_times と closing_times の要素の順番が予め対応して計算される場合
    * opening_times と closing_times の要素の個数や順番を対応させる必要がある場合
    """

    def __init__(self, indicators_are_corresponded):
        super().__init__()
        self.__indicators_are_corresponded = indicators_are_corresponded
        # 子の戦略から変更できるように public にしている。
        self.using_cython = True

    def calculate_closing_times(self, df, opening_times):
        # open
        # long, short それぞれで昇順になっている。
        opening_times_long, opening_times_short = opening_times

        # close
        # long, short それぞれで昇順になっている。
        closing_times_long, \
        closing_times_short = self.calculate_independent_closing_times(df)

        # long
        closing_times_long = \
            self.__convert_independent_closing_times_to_dependent_ones(
                opening_times_long, closing_times_long)

        # short
        closing_times_short = \
            self.__convert_independent_closing_times_to_dependent_ones(
                opening_times_short, closing_times_short)

        return closing_times_long, closing_times_short

    def calculate_times(self, df):
        opening_times = self.calculate_opening_times(df)
        
        # opening_times と closing_times の要素の順が既に対応している場合、
        # 計算コストを削減できるので、場合分けしている。
        if self.__indicators_are_corresponded:
            closing_times = self.calculate_independent_closing_times(df)
        else:
            closing_times = self.calculate_closing_times(df, opening_times)

        return opening_times, closing_times

    def calculate_independent_closing_times(self, df):
        close_indicators = self.calculate_close_indicators(df)

        # long
        can_close_long = self.convert_close_indicators(
            close_indicators, position_type='long')
        closing_times_long = self._specify_closing_times(can_close_long)
        
        # short
        can_close_short = self.convert_close_indicators(
            close_indicators, position_type='short')        
        closing_times_short = self._specify_closing_times(can_close_short)

        return closing_times_long, closing_times_short

    def __convert_independent_closing_times_to_dependent_ones(
            self, opening_times, closing_times):
        if self.using_cython:
            return self.__convert_with_cython(opening_times, closing_times)
        else:
            return self.__convert_with_python(opening_times, closing_times)

    def __convert_with_cython(self, opening_times, closing_times):
        opening_timestamps = list(map(
            lambda x: dt.strptime(x, self.time_format).timestamp(),
            opening_times))
        closing_timestamps = list(map(
            lambda x: dt.strptime(x, self.time_format).timestamp(),
            closing_times))
        closing_times = list(closing_times)
        return convert_with_cython(
            opening_timestamps, closing_timestamps, closing_times)

    def __convert_with_python(self, opening_times, closing_times):
        def create_specifying(closing_times):
            @np.vectorize
            def _specify(opening_time):
                indicator = closing_times > opening_time
                can_trade = pd.concat(
                    [indicator[1:],
                     indicator.shift(1)[1:].apply(lambda x: not(x))],
                    axis=1).all(axis=1)

                can_trade = can_trade[can_trade]
                if len(can_trade) == 0:
                    return None

                # ここで Timestamp 型から str に変換すると、
                # None も 'None' に変換されてしまうことに注意。
                trade_time = str(can_trade.index[0])
                return trade_time
            return _specify

        closing_times = pd.DataFrame(closing_times, columns=['closing_time'])
        closing_times['closing_time'] = \
            pd.to_datetime(closing_times['closing_time'])
        closing_times.index = closing_times['closing_time']

        opening_times = pd.DataFrame(opening_times, columns=['opening_time'])
        opening_times['opening_time'] = \
            pd.to_datetime(opening_times['opening_time'])
        opening_times.index = opening_times['opening_time']

        start = opening_times.head(1).index[0]
        end = closing_times.tail(1).index[0]
        time_index = pd.date_range(start=start, end=end, freq=self.frequency)
        closing_times = closing_times.reindex(time_index)

        specify = create_specifying(closing_times['closing_time'])
        ccts = specify(opening_times['opening_time'])

        # None が 'None' になってしまっているため
        dependent_closing_times = np.where(ccts == 'None', None, ccts)

        return dependent_closing_times