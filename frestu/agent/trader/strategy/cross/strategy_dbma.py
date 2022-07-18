from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDbma


class StrategyDbma(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorDbma(
            ma_type_shorter, window_shorter, ma_type_longer, window_longer)

    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df).iloc[:, 0]