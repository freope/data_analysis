import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract


class StrategyMau(StrategyContinuousIndicatorAbstract):
    """
    Moving Averages Unanimous
    """

    def __init__(self, windows, shift=1, prefix='ma_'):
        """
        複数の移動平均を計算する為のパラメータを初期化

        Parameters
        ----------
        windows : list of int
            複数の移動平均の窓サイズが格納されたリスト
        shift : int
            移動平均曲線の傾きを計算する際に、何時点前と差分を取るか
        suffix : str
            移動平均のカラム名の接頭辞

        Returns
        -------
        None
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
        elif position_type == 'short':
            is_falling = (indicators < 0).all(axis=1)
            return is_falling