from frestu.agent.trader.strategy import StrategyAbstract


class StrategyCombinatorOpenAndClose(StrategyAbstract):
    
    def __init__(self, open_strategy, close_strategy):
        super().__init__()
        self.__open_strategy = open_strategy
        self.__close_strategy = close_strategy
    
    def calculate_opening_times(self, df):
        return self.__open_strategy.calculate_opening_times(df)

    def calculate_closing_times(self, df, opening_times):
        return self.__close_strategy.calculate_closing_times(df, opening_times)

    def calculate_times(self, df):
        opening_times = self.calculate_opening_times(df)
        closing_times = self.calculate_closing_times(df, opening_times)
        return opening_times, closing_times