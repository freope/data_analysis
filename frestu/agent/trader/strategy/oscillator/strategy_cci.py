from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorCci
from frestu.feature_extraction.time_series import ExtractorDfma


class StrategyCci(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            window_dfsma, window_cci, window_ohlc,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_dfsma = ExtractorDfma('sma', window_dfsma)
        self.__extractor_cci = ExtractorCci(window_cci, window_ohlc)

    def calculate_open_indicators(self, df):
        cci = self.__extractor_cci.extract(df)
        dfsma_cci = self.__extractor_dfsma.extract(cci)
        return dfsma_cci