import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract


class StrategyCombinatorSimultaneousOpen(StrategyAbstract):
    
    def __init__(self, time_buffer, strategy_0, strategy_1):
        super().__init__()
        self.__time_buffer = time_buffer
        self.__strategy_0 = strategy_0
        self.__strategy_1 = strategy_1

    def calculate_opening_times(self, df):
        start = df.head(1).index[0]
        end = df.tail(1).index[0]
        time_index = pd.date_range(start=start, end=end, freq=self.frequency)

        opening_times_0 = self.__strategy_0.calculate_opening_times(df)
        opening_times_1 = self.__strategy_1.calculate_opening_times(df)

        # long
        opening_times_long = self.__convert_opening_times_to_simultaneous_ones(
            opening_times_0[0], opening_times_1[0], time_index)

        # short
        opening_times_short = self.__convert_opening_times_to_simultaneous_ones(
            opening_times_0[1], opening_times_1[1], time_index)
    
        return opening_times_long, opening_times_short

    def calculate_closing_times(self, df, opening_times):
        pass
    
    def calculate_times(self, df):
        pass

    def __convert_opening_times_to_simultaneous_ones(
            self, opening_times_0, opening_times_1, time_index):
        
        indicator = self.__calculate_open_indicators(
            opening_times_0, opening_times_1, time_index)

        can_open = pd.concat(
            [indicator[1:], indicator.shift(1)[1:].apply(lambda x: not(x))],
            axis=1).all(axis=1)

        can_open = can_open[can_open]
        if len(can_open) == 0:
            return []

        opening_times = list(can_open.index.map(lambda x: str(x)))

        return opening_times
    
    def __calculate_open_indicators(
            self, opening_times_0, opening_times_1, time_index):
        can_open_0 = self.__can_open(opening_times_0, time_index)
        can_open_1 = self.__can_open(opening_times_1, time_index)
        indicator = pd.concat([can_open_0, can_open_1], axis=1).all(axis=1)
        return indicator

    def __can_open(self, opening_times, time_index):
        opening_times = pd.DataFrame(opening_times, columns=['opening_time'])
        opening_times['opening_time'] = pd.to_datetime(
            opening_times['opening_time'])
        opening_times.index = opening_times['opening_time']
        opening_times = opening_times.reindex(time_index)

        can_open = ~np.isnan(opening_times)

        for i in range(1, self.__time_buffer+1):
            can_open |= can_open.shift(i)

        return can_open