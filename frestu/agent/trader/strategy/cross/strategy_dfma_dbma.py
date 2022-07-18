from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDfma
from frestu.feature_extraction.time_series import ExtractorDbma


class StrategyDfmaDbma(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            ma_type_dfma, window, 
            ma_type_dbma_shorter, window_shorter,
            ma_type_dbma_longer, window_longer,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_dfema = ExtractorDfma(ma_type_dfma, window)
        self.__extractor_dbema = ExtractorDbma(
            ma_type_dbma_shorter, window_shorter,
            ma_type_dbma_longer, window_longer)

    def calculate_open_indicators(self, df):
        return self.__extractor_dfema.extract(
            self.__extractor_dbema.extract(df)).iloc[:, 0]