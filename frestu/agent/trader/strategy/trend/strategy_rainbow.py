import pandas as pd

from frestu.agent.trader.strategy import StrategyIndependentCloseAbstract
from frestu.feature_extraction.time_series import ExtractorMa


class StrategyRainbow(StrategyIndependentCloseAbstract):
    
    def __init__(self, ma_type, window_shorter, window_medium, window_longer):
        super().__init__(indicators_are_corresponded=False)
        self.__extractor_shorter = ExtractorMa(ma_type, window_shorter)
        self.__extractor_medium = ExtractorMa(ma_type, window_medium)
        self._extractor_longer = ExtractorMa(ma_type, window_longer)
    
    def calculate_open_indicators(self, df):
        ma_shorter = self.__extractor_shorter.extract(df)
        ma_medium = self.__extractor_medium.extract(df)
        ma_longer = self._extractor_longer.extract(df)
        slope_shorter = ma_shorter - ma_shorter.shift(1)

        # long
        condition_long_1 = ma_shorter > ma_medium
        condition_long_2 = ma_medium > ma_longer
        condition_long_3 = slope_shorter < 0
        condition_long_4 = df < ma_medium

        can_open_long = pd.concat([
            condition_long_1,
            condition_long_2,
            condition_long_3,
            condition_long_4,
        ], axis=1).all(axis=1)

        # short
        condition_short_1 = ma_shorter < ma_medium
        condition_short_2 = ma_medium < ma_longer
        condition_short_3 = slope_shorter > 0
        condition_short_4 = df > ma_medium

        can_open_short = pd.concat([
            condition_short_1,
            condition_short_2,
            condition_short_3,
            condition_short_4,
        ], axis=1).all(axis=1)

        can_open = pd.concat([can_open_long, can_open_short], axis=1)
        can_open.columns = ['long', 'short']
        
        return can_open

    def calculate_close_indicators(self, df):
        """
        Notes
        -----
        エントリーと同時に利確エクジットの condition_1 が満たされている場合があるが、
        False から True に変わる時刻を _specify_closing_times で抽出することで、
        エントリーした直後にエクジットになることを防いでいる。
        しかし、その場合、そのままレートが逆行すると、損切りエクジットの condition_2 の
        発動も阻止され、損切りされないままになってしまう。なので、損切りエクジットの前の時刻を
        False にすることで、必ず損切りが発動するようにした。
        """

        ma_shorter = self.__extractor_shorter.extract(df)
        ma_longer = self._extractor_longer.extract(df)

        # long
        # 利確
        condition_long_1 = ma_shorter > df
        # 損切り
        condition_long_2 = ma_shorter < ma_longer

        can_close_long = pd.concat([
            condition_long_1,
            condition_long_2,
        ], axis=1).any(axis=1)

        # 損切り発動直前の時刻を False にしておく。
        should_be_false_long = pd.concat(
            [condition_long_2.shift(-1)[:-1], ~condition_long_2[:-1]],
            axis=1).all(axis=1)
        can_close_long = can_close_long.where(~should_be_false_long, False)

        # short
        # 利確
        condition_short_1 = ma_shorter < df
        # 損切り
        condition_short_2 = ma_shorter > ma_longer

        can_close_short = pd.concat([
            condition_short_1,
            condition_short_2,
        ], axis=1).any(axis=1)

        # 損切り発動直前の時刻を False にしておく。
        should_be_false_short = pd.concat(
            [condition_short_2.shift(-1)[:-1], ~condition_short_2[:-1]],
            axis=1).all(axis=1)
        can_close_short = can_close_short.where(~should_be_false_short, False)

        can_close = pd.concat(
            [can_close_long, can_close_short], axis=1)
        can_close.columns = ['long', 'short']

        return can_close
    
    def convert_open_indicators(self, indicators, position_type):
        return indicators[position_type]

    def convert_close_indicators(self, indicators, position_type):
        return indicators[position_type]
    
    def _specify_closing_times(self, can_close):
        if can_close.shape[0] == 0:
            return []
        return self._specify_trade_times(can_close)