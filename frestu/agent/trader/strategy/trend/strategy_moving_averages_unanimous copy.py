import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract


class StrategyMovingAveragesUnanimous(StrategyAbstract):

    def __init__(self, windows_width, shift=1, prefix='ma_', freq='min'):
        """
        複数の移動平均を計算する為のパラメータを初期化

        Parameters
        ----------
        windows_width : list of int
            複数の移動平均の窓サイズが格納されたリスト
        shift : int
            移動平均曲線の傾きを計算する際に、何時点前と差分を取るか
        suffix : str
            移動平均のカラム名の接頭辞
        freq : str
            サンプリング周期

        Returns
        -------
        None
        """
        super().__init__()
        self.__windows_width = windows_width
        self.__shift = shift
        self.__prefix = prefix
        self.__freq = freq
    
    def calculate_open_positions(self, df):
        indicators = self.calculate_indicators(df)
        
        # long
        long_positions = []
        candidates = indicators[(indicators > 0).all(axis=1)]
        if candidates.shape[0] != 0:
            candidates = self.__narrow_down_open_position_candidates(candidates)
            long_positions = [
                {'position_type': 'long', 'opening_time': str(opening_time)}
                for opening_time in candidates.index]
        # short
        short_positions = []
        candidates = indicators[(indicators < 0).all(axis=1)]
        if candidates.shape[0] != 0:
            candidates = self.__narrow_down_open_position_candidates(candidates)
            short_positions = [
                {'position_type': 'short', 'opening_time': str(opening_time)}
                for opening_time in candidates.index]
        open_positions = long_positions + short_positions
        return open_positions

    def calculate_closing_times(self, df, open_positions):
        indicators = self.calculate_indicators(df)

        closing_times = []
        for open_position in open_positions:
            position_type = open_position['position_type']
            opening_time = open_position['opening_time']
            candidates = indicators[f'{opening_time}':]
            candidates.index = pd.to_datetime(candidates.index)
            if position_type == 'long':
                positions = candidates[(candidates > 0).all(axis=1)]
            elif position_type == 'short':
                positions = candidates[(candidates < 0).all(axis=1)]
            closing_time = self.__narrow_down_closing_time_candidates(
                candidates, positions)
            closing_times.append(closing_time)
        return closing_times

    def calculate_closed_positions(self, df):
        indicators = self.calculate_indicators(df)

        # 一括計算の際は、ここで start, end を取得しないと、最も新しい時刻端で
        # closing_times の数が足りなくり得る。
        start = indicators.head(1).index[0]
        end = indicators.tail(1).index[0]

        # long
        long_positions = []
        candidates = indicators[(indicators > 0).all(axis=1)]
        if candidates.shape[0] != 0:
            op_candidates, ct_candidates = \
                self.__narrow_down_closed_position_candidates(
                    candidates, start, end)
            long_positions = [
                {'position_type': 'long', 'opening_time': str(opening_time)}
                for opening_time in op_candidates.index]
            long_closing_times = [
                str(closing_time)
                for closing_time in ct_candidates.index]
        # short
        short_positions = []
        candidates = indicators[(indicators < 0).all(axis=1)]
        if candidates.shape[0] != 0:
            op_candidates, ct_candidates = \
                self.__narrow_down_closed_position_candidates(
                    candidates, start, end)
            short_positions = [
                {'position_type': 'short', 'opening_time': str(opening_time)}
                for opening_time in op_candidates.index]
            short_closing_times = [
                str(closing_time)
                for closing_time in ct_candidates.index]
        # 建玉を捨てる
        open_positions = long_positions[:len(long_closing_times)] \
            + short_positions[:len(short_closing_times)]
        closing_times = long_closing_times + short_closing_times
        return open_positions, closing_times

    def calculate_indicators(self, df):
        dfs = []
        columns_name = []
        for window_width in self.__windows_width:
            dfs.append(df.rolling(window_width).mean())
            columns_name.append(self.__prefix + str(window_width))
        dfs = pd.concat(dfs, axis=1)
        dfs.columns = columns_name
        dfs_diff = dfs - dfs.shift(self.__shift)
        # dfs_diff = dfs_diff.dropna()
        return dfs_diff

    def __narrow_down_open_position_candidates(self, candidates):
        start = candidates.head(1).index[0]
        end = candidates.tail(1).index[0]
        time_index = pd.date_range(start=start, end=end, freq=self.__freq)
        candidates.index = pd.to_datetime(candidates.index)
        candidates = candidates.reindex(time_index)
        
        # 全ての列が NaN でない行のうち、全ての列が NaN である行が
        # 1 時刻前にある行が、取引開始の行である。
        all_nan_shifted = np.isnan(candidates.shift(1)).all(axis=1)
        not_all_nan = ~np.isnan(candidates).all(axis=1)
        can_have_position = pd.concat(
            [not_all_nan, all_nan_shifted], axis=1).all(axis=1)
        return candidates[can_have_position]
    
    def __narrow_down_closing_time_candidates(self, candidates, positions):
        start = candidates.head(1).index[0]
        end = candidates.tail(1).index[0]
        time_index = pd.date_range(start=start, end=end, freq=self.__freq)
        positions = positions.reindex(time_index)

        closing_time_candidates = positions[np.isnan(positions).all(axis=1)]
        # まだクローズ注文をすべきでない場合は None を返す
        if len(closing_time_candidates) == 0:
            return None
        closing_time = str(closing_time_candidates.index[0])
        return closing_time

    def __narrow_down_closed_position_candidates(self, candidates, start, end):
        time_index = pd.date_range(start=start, end=end, freq=self.__freq)
        candidates.index = pd.to_datetime(candidates.index)
        candidates = candidates.reindex(time_index)

        # 全ての列が NaN でない行のうち、全ての列が NaN である行が
        # 1 時刻前にある行が、取引開始の行である。
        all_nan_shifted = np.isnan(candidates.shift(1)).all(axis=1)
        not_all_nan = ~np.isnan(candidates).all(axis=1)
        can_have_position = pd.concat(
            [not_all_nan, all_nan_shifted], axis=1).all(axis=1)
        
        # 全ての列が NaN である行のうち、全ての列が NaN でない行が
        # 1 時刻前にある行が、取引終了の行である。
        all_nan = np.isnan(candidates).all(axis=1)
        not_all_nan_shifted = ~np.isnan(candidates.shift(1)).all(axis=1)
        can_leave_position = pd.concat(
            [all_nan, not_all_nan_shifted], axis=1).all(axis=1)

        return candidates[can_have_position], candidates[can_leave_position]