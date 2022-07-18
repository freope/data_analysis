from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract
from frestu.feature_extraction.time_series import ExtractorParabolicSar


class StrategyParabolicSar(StrategyCrossIndicatorsAbstract):

    def __init__(self, step_af, af_max, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__extractor = ExtractorParabolicSar(step_af, af_max)

    def calculate_open_indicators(self, df):
        parabolic_sar = self.__extractor.extract(df)
        indicator = df.iloc[:, 0] - parabolic_sar.iloc[:, 0]
        return indicator