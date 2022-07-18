from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorHeikinashi


class StrategyHeikinashiCrossRawHa(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            window, col_rate, col_ha,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__col_rate = col_rate
        self.__col_ha = col_ha
        self.__extractor = ExtractorHeikinashi(window)
    
    def calculate_open_indicators(self, df):
        ha = self.__extractor.extract(df)
        indicator = df.loc[:, self.__col_rate] - ha.loc[:, self.__col_ha]
        return indicator