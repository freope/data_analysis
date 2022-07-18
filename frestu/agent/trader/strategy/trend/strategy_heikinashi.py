from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorHeikinashi


class StrategyHeikinashi(StrategyCrossIndicatorsAbstract):

    def __init__(self, window, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorHeikinashi(window)
    
    def calculate_open_indicators(self, df):
        ha = self.__extractor.extract(df)
        indicator = ha.loc[:, 'ha_closing'] - ha.loc[:, 'ha_open']
        return indicator