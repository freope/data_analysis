from abc import abstractmethod

import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract


class StrategyComponentAbstract(StrategyAbstract):

    def calculate_opening_times(self, df):
        open_indicators = self.calculate_open_indicators(df)

        can_open_long = self.convert_open_indicators(
            open_indicators, position_type='long')
        opening_times_long = self._specify_opening_times(can_open_long)

        can_open_short = self.convert_open_indicators(
            open_indicators, position_type='short')
        opening_times_short = self._specify_opening_times(can_open_short)

        # long, short それぞれで昇順になっている。
        return opening_times_long, opening_times_short

    @abstractmethod
    def calculate_open_indicators(self, df):
        pass

    @abstractmethod
    def convert_open_indicators(self, indicators, position_type):
        pass

    @abstractmethod
    def calculate_close_indicators(self, df, positions):
        pass

    @abstractmethod
    def convert_close_indicators(self, indicators, position_type):
        pass

    def _specify_opening_times(self, can_open):
        if can_open.shape[0] == 0:
            return []
        return self._specify_trade_times(can_open)

    @abstractmethod
    def _specify_closing_times(self, can_close):
        pass

    def _specify_trade_times(self, can_trade):
        # NOTE: 2021/04/07 まで以下のコードを使っていた。
        # can_trade = pd.concat(
        #     [can_trade[1:], can_trade.shift(1)[1:].apply(lambda x: not(x))],
        #     axis=1).all(axis=1)
        # NOTE: 以下でも、良いかも。
        # can_trade = can_trade[1:] * (~can_trade.shift(1)[1:]) == -1
        # NOTE: 以下だと、複数カラムでエラーが出ないので、エラー処理が必要になる。
        if len(can_trade.shape) != 1:
            raise ValueError('should be len(can_trade.shape) == 1')
        can_trade = can_trade[1:] * (can_trade.shift(1)[1:] == False)

        can_trade = can_trade[can_trade]
        if len(can_trade) == 0:
            return []

        trade_times = list(can_trade.index)
        return trade_times