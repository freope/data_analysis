from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsBoundedAbstract
from frestu.feature_extraction.time_series import ExtractorDfma


class StrategyDfmaBounded(StrategyCrossIndicatorsBoundedAbstract):

    def __init__(
            self,
            ma_type, window,
            bound_long, bound_short,
            threshold_long=0, threshold_short=0):
        """
        Notes
        -----
        calculate_closing_times() だけを使う前提の戦略。
        """
        super().__init__(
            bound_long, bound_short, threshold_long, threshold_short)
        self.__extractor = ExtractorDfma(ma_type, window)

    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df).iloc[:, 0]