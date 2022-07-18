from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorsAbstract


class StrategyCrossIndicatorsAlreadyCalculated(StrategyCrossIndicatorsAbstract):

    def __init__(self, indicators, threshold_long=0, threshold_short=0):
        super().__init__(threshold_long, threshold_short)
        self.__indicators = indicators

    def calculate_open_indicators(self, df):
        return self.__indicators.loc[df.index, :].iloc[:, 0]