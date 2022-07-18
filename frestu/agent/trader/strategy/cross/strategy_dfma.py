from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDfma


class StrategyDfma(StrategyCrossIndicatorsAbstract):

    def __init__(self, ma_type, window, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorDfma(ma_type, window)

    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df).iloc[:, 0]