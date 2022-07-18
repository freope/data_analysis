from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series.stochastic_process import ExtractorLocalLevelSequentialSmooth


class StrategyLocalLevelCrossSmooths(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            col_rate, lag_shorter, lag_longer, m0, C0, dW, dV,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_shorter = ExtractorLocalLevelSequentialSmooth(
            col_rate, lag_shorter, m0, C0, dW, dV)
        self.__extractor_longer = ExtractorLocalLevelSequentialSmooth(
            col_rate, lag_longer, m0, C0, dW, dV)

    def calculate_open_indicators(self, df):
        mu_s = self.__extractor_shorter.extract(df)
        mu_l = self.__extractor_longer.extract(df)
        indicator = mu_s['mu_sequential_smooth'] - mu_l['mu_sequential_smooth']
        return indicator