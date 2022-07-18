from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract


class StrategyPartSettableExtractor(StrategyCrossIndicatorsAbstract):

    def __init__(self, extractor, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = extractor

    def calculate_open_indicators(self, df):
        return self.__extractor.extract(df)