import pandas as pd

from frestu.agent.trader.strategy import StrategyComponentAbstract


class StrategyDependentCloseAbstract(StrategyComponentAbstract):

    def calculate_closing_times(self, df, opening_times):
        """
        Notes
        -----
        closing_times が opening_times に依存する形でしか計算できないクラス。
        opening_time のレートによって closing_time が変化する場合など。
        xxx_opening_times と can_close_xxx が対応したキュー構造。
        calculate_close_indicators と convert_close_indicators を、
        そうなるように設計する必要がある。
        """
        # long
        opening_times_long = opening_times[0]
        close_indicators_long = self.calculate_close_indicators(
            df, opening_times_long)
        can_close_long = self.convert_close_indicators(
            close_indicators_long, position_type='long')
        closing_times_long = self._specify_closing_times(can_close_long)

        # short
        opening_times_short = opening_times[1]
        close_indicators_short = self.calculate_close_indicators(
            df, opening_times_short)
        can_close_short = self.convert_close_indicators(
            close_indicators_short, position_type='short')        
        closing_times_short = self._specify_closing_times(can_close_short)

        return closing_times_long, closing_times_short

    def calculate_times(self, df):
        """
        Notes
        -----
        opening_times と closing_times の要素の順が対応している必要がある。
        建玉がある場合、
        1. 対応する closing_time の値を None にするか、
        2. opening_times の 末尾に建玉の opening_time が入っている
        必要がある。1, 2 を同時に使うこともできる。
        2 の場合、closing_times より opening_times の要素数が多いことになる。
        """
        opening_times = self.calculate_opening_times(df)
        closing_times = self.calculate_closing_times(df, opening_times)
        return opening_times, closing_times