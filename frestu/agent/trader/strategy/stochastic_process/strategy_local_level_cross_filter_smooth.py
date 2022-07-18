from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series.stochastic_process import ExtractorLocalLevelSequentialSmooth


class StrategyLocalLevelCrossFilterSmooth(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            col_rate, lag, m0, C0, dW, dV,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorLocalLevelSequentialSmooth(
            col_rate, lag, m0, C0, dW, dV, True)

    def calculate_open_indicators(self, df):
        mu = self.__extractor.extract(df)
        indicator = mu['mu_filter'] - mu['mu_sequential_smooth']
        return indicator