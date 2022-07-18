from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series.stochastic_process import ExtractorLocalLevel


class StrategyLocalLevelCrossRawFilter(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            col_rate, m0, C0, dW, dV,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__col_rate = col_rate
        self.__extractor = ExtractorLocalLevel(col_rate, m0, C0, dW, dV)

    def calculate_open_indicators(self, df):
        mu = self.__extractor.extract(df)
        indicator = df[self.__col_rate] - mu['mu_filter']
        return indicator