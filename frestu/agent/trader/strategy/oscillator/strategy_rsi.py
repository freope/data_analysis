from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract
from frestu.feature_extraction.time_series import ExtractorRsi


class StrategyRsi(StrategyContinuousIndicatorAbstract):

    def __init__(self, window, threshold_long, threshold_short):
        super().__init__()
        self.__extractor = ExtractorRsi(window)
        self.__threshold_long = threshold_long
        self.__threshold_short = threshold_short
    
    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df).iloc[:, 0]
    
    def convert_open_indicators(self, indicators, position_type):
        if position_type == 'long':
            is_rising = indicators > self.__threshold_long
            return is_rising
        elif position_type == 'short':
            is_falling = indicators < self.__threshold_short
            return is_falling