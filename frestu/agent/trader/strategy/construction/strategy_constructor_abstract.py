from abc import abstractmethod
from frestu.agent.trader.strategy import StrategyAbstract


class StrategyConstructorAbstract(StrategyAbstract):

    @abstractmethod
    def __init__(self):
        pass
    
    def calculate_opening_times(self, df):
        return self._strategy.calculate_opening_times(df)
    
    def calculate_closing_times(self, df, opening_times):
        return self._strategy.calculate_closing_times(df, opening_times)
    
    def calculate_times(self, df):
        return self._strategy.calculate_times(df)
