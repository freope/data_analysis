import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyDependentCloseAbstract


class StrategyMauDependentClose(StrategyDependentCloseAbstract):

    def __init__(self, windows, shift=1, prefix='ma_'):
        """
        StrategyIndependentClose を継承したクラスの実装練習用。
        もともとは、StrategyContinuousIndicatorAbstract を継承して実装するもの。
        """
        super().__init__()
        self.__windows = windows
        self.__shift = shift
        self.__prefix = prefix

    def calculate_open_indicators(self, df):
        dfs = []
        columns_name = []
        for window in self.__windows:
            dfs.append(df.rolling(window).mean())
            columns_name.append(self.__prefix + str(window))
        dfs = pd.concat(dfs, axis=1)
        dfs.columns = columns_name
        dfs_diff = dfs - dfs.shift(self.__shift)
        # dropna すると、先頭の行を検出できなくなるので。
        # dfs_diff = dfs_diff.dropna()
        return dfs_diff

    def convert_open_indicators(self, indicators, position_type):
        if position_type == 'long':
            is_rising = (indicators > 0).all(axis=1)
            return is_rising
        is_falling = (indicators < 0).all(axis=1)
        return is_falling

    def calculate_close_indicators(self, df, opening_times):
        return self.calculate_open_indicators(df), len(opening_times)

    def convert_close_indicators(self, indicators, position_type):
        indicator, len_opening_times = indicators
        return (~self.convert_open_indicators(indicator, position_type),
                len_opening_times)

    def _specify_closing_times(self, can_close):
        can_close, len_opening_times = can_close
        closing_times = list(self._specify_trade_times(can_close))
        for _ in range(len_opening_times - len(closing_times)):
            closing_times.append(None)
        return closing_times