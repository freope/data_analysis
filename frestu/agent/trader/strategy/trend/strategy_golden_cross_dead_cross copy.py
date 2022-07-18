from datetime import datetime as dt

import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract


class StrategyGoldenCrossDeadCross(StrategyAbstract):

    def __init__(
            self,
            shorter_window_width, longer_window_width,
            time_format='%Y-%m-%d %H:%M:%S'):
        """
        複数の移動平均を計算する為のパラメータを初期化

        Parameters
        ----------
        shorter_window_width: int
            移動平均の短い方の窓サイズ
        longer_window_width: int
            移動平均の長い方の窓サイズ
        time_format : str
            データの時刻のフォーマット。時刻を比較するために用いる。

        Returns
        -------
        None
        """
        if not shorter_window_width < longer_window_width:
            raise ValueError(
                'should be shorter_window_width < longer_window_width.')
        self.__shorter_window_width = shorter_window_width
        self.__longer_window_width = longer_window_width
        self.__time_format = time_format

    def calculate_closing_times(self, df, open_positions):
        indicators = self.calculate_indicators(df)

        closing_times = []
        for open_position in open_positions:
            position_type = open_position['position_type']
            opening_time = open_position['opening_time']

            candidates = indicators[f'{opening_time}':]
            candidates.index = pd.to_datetime(candidates.index)

            if position_type == 'long':
                is_waiting_for_dead = candidates < 0
                can_leave_position = ~is_waiting_for_dead
            elif position_type == 'short':
                is_waiting_for_golden = candidates > 0
                can_leave_position = ~is_waiting_for_golden

            can_leave_position = can_leave_position[can_leave_position]

            # まだクローズ注文をすべきでない場合は None を返す
            if len(can_leave_position) == 0:
                closing_time = None
            else:
                closing_time = can_leave_position.index[0]
                closing_time = str(closing_time)

            closing_times.append(closing_time)

        return closing_times

    def calculate_closed_positions(self, df):
        indicators = self.calculate_indicators(df)

        long_open_positions = self._calculate_long_open_positions(indicators)
        long_open_position = long_open_positions[0]
        long_opening_time = long_open_position['opening_time']
        long_opening_time = dt.strptime(long_opening_time, self.__time_format)

        short_open_positions = self._calculate_short_open_positions(indicators)
        short_open_position = short_open_positions[0]
        short_opening_time = short_open_position['opening_time']
        short_opening_time = dt.strptime(short_opening_time, self.__time_format)

        if long_opening_time < short_opening_time:
            long_closing_times = list(map(
                lambda x: x['opening_time'], short_open_positions))
            short_closing_times = list(map(
                lambda x: x['opening_time'], long_open_positions[1:]))
        else:
            long_closing_times = list(map(
                lambda x: x['opening_time'], short_open_positions[1:]))
            short_closing_times = list(map(
                lambda x: x['opening_time'], long_open_positions))

        closing_times = long_closing_times + short_closing_times

        # 建玉を捨てる
        open_positions = long_open_positions[:len(long_closing_times)] \
            + short_open_positions[:len(short_closing_times)]

        return open_positions, closing_times
    
    def calculate_indicators(self, df):
        dfs = [
            df.rolling(self.__shorter_window_width).mean(),
            df.rolling(self.__longer_window_width).mean()]
        columns_name = ['shorter', 'longer']
        dfs = pd.concat(dfs, axis=1)
        dfs.columns = columns_name
        ma_diff = dfs['longer'] - dfs['shorter']
        # NaN も大小比較によって True/False に変換され、
        # 正常な値を区別出来なくなるので、ここで NaN を落とす。
        ma_diff = ma_diff.dropna()
        return ma_diff

    def _convert_indicators_to_long_candidates(self, indicators):
        is_waiting_for_golden = indicators > 0
        return is_waiting_for_golden

    def _convert_indicators_to_short_candidates(self, indicators):
        is_waiting_for_dead = indicators < 0
        return is_waiting_for_dead

    def _calculate_opening_times(self, candidates):
        can_have_position = pd.concat(
            [~candidates[1:], candidates.shift(1)[1:]],
            axis=1).all(axis=1)
        can_have_position = can_have_position[can_have_position]
        if len(can_have_position) == 0:
            return []
        opening_times = can_have_position.index
        return opening_times
    
    def _calculate_closing_times(self, candidates):
        pass

    def _calculate_long_open_positions(self, indicators):
        is_waiting_for_golden = indicators > 0

        can_have_position = pd.concat(
            [~is_waiting_for_golden[1:],
             is_waiting_for_golden.shift(1)[1:]],
            axis=1).all(axis=1)
        can_have_position = can_have_position[can_have_position]

        if len(can_have_position) == 0:
            opening_times = []
        else:
            opening_times = can_have_position.index

        long_open_positions = [
            {'position_type': 'long', 'opening_time': str(opening_time)}
            for opening_time in opening_times]

        return long_open_positions

    def _calculate_short_open_positions(self, indicators):
        is_waiting_for_golden = indicators > 0
        
        can_have_position = pd.concat(
            [is_waiting_for_golden[1:],
             is_waiting_for_golden.shift(1)[1:].apply(lambda x: not(x))],
            axis=1).all(axis=1)
        can_have_position = can_have_position[can_have_position]

        if len(can_have_position) == 0:
            opening_times = []
        else:
            opening_times = can_have_position.index

        short_open_positions = [
            {'position_type': 'short', 'opening_time': str(opening_time)}
            for opening_time in opening_times]

        return short_open_positions