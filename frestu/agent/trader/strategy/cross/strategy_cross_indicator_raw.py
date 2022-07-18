from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract


class StrategyCrossIndicatorRaw(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            extractor, col_indicator, col_raw,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = extractor
        self.__col_indicator = col_indicator
        self.__col_raw = col_raw

    def calculate_open_indicators(self, df):
        feature = self.__extractor.extract(df)
        feature = feature[self.__col_indicator] - df[self.__col_raw]
        return feature