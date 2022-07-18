from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorDmi


class StrategyDmiDi(StrategyCrossIndicatorsAbstract):

    def __init__(
            self,
            window_ohlc, window_tr_dm,
            threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorDmi(window_ohlc, window_tr_dm)

    def calculate_open_indicators(self, df):
        dmi = self.__extractor.extract(df)
        indicators = dmi['+DI'] - dmi['-DI']
        return indicators