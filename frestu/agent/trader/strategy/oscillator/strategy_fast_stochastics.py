from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorStochastics


class StrategyFastStochastics(StrategyCrossIndicatorsAbstract):

    def __init__(self, x, y, z, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorStochastics(x, y, z)

    def calculate_open_indicators(self, df):
        stochastics = self.__extractor.extract(df)
        indicators = stochastics['%K'] - stochastics['%D']
        return indicators