from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract


class StrategyCrossIndicators(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            extractor_minuend, cols_minuend_in, col_minuend_out,
            extractor_subtrahend, cols_subtrahend_in, col_subtrahend_out,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor_minuend = extractor_minuend
        self.__cols_minuend_in = cols_minuend_in
        self.__col_minuend_out = col_minuend_out
        self.__extractor_subtrahend = extractor_subtrahend
        self.__cols_subtrahend_in = cols_subtrahend_in
        self.__col_subtrahend_out = col_subtrahend_out

    def calculate_open_indicators(self, df):
        m = self.__extractor_minuend.extract(df[self.__cols_minuend_in])
        s = self.__extractor_subtrahend.extract(df[self.__cols_subtrahend_in])
        feature = m[self.__col_minuend_out] - s[self.__col_subtrahend_out]
        return feature