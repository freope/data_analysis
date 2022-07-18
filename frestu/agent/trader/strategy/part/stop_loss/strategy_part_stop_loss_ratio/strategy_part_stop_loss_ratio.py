import pyximport
pyximport.install()

import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract
from frestu.agent.trader.strategy.part.stop_loss.strategy_part_stop_loss_ratio.calculate_with_cython import calculate_with_cython


class StrategyPartStopLossRatio(StrategyAbstract):
    
    def __init__(self, stopping_ratio):
        super().__init__()
        self.__stopping_ratio = stopping_ratio
        self.using_cython = True

    def calculate_opening_times(self, df):
        pass
    
    def calculate_closing_times(self, df, opening_times):
        # open
        opening_times_long, opening_times_short = opening_times

        # long
        closing_times_long = self.__calculate_closing_times(
            df, opening_times_long, position_type='long')

        # short
        closing_times_short = self.__calculate_closing_times(
            df, opening_times_short, position_type='short')

        return closing_times_long, closing_times_short

    def calculate_times(self, df):
        pass

    def __calculate_closing_times(self, df, opening_times, position_type):
        if self.using_cython:
            return self.__calculate_with_cython(
                df, opening_times, position_type)
        else:
            return self.__calculate_with_python(
                df, opening_times, position_type)

    def __calculate_with_cython(self, df, opening_times, position_type):
        rates = list(df.iloc[:, 0])
        time_to_ix = dict([[t, i] for i, t in enumerate(df.index)])
        ix_to_time = dict([[i, t] for i, t in enumerate(df.index)])
        return calculate_with_cython(
            opening_times, rates, time_to_ix, ix_to_time,
            self.__stopping_ratio, position_type)

    def __calculate_with_python(self, df, opening_times, position_type):
        opening_times = pd.DataFrame(opening_times, columns=['opening_time'])
        specify = self.__create_specifying(df, position_type)
        closing_times = specify(opening_times['opening_time'])
        return np.where(closing_times == 'None', None, closing_times)

    def __create_specifying(self, df, position_type):
        @np.vectorize
        def _specify(opening_time):
            opening_rate = df.loc[opening_time][0]
                    
            if position_type == 'long':
                stop_loss_rate = opening_rate * (1 - self.__stopping_ratio)
                indicators = df[opening_time:] <= stop_loss_rate
            elif position_type == 'short':
                stop_loss_rate = opening_rate * (1 + self.__stopping_ratio)   
                indicators = df[opening_time:] >= stop_loss_rate
            
            indicators = indicators.iloc[:, 0]
            can_close = pd.concat(
                [indicators[1:], 
                indicators.shift(1)[1:].apply(lambda x: not(x))],
                axis=1).all(axis=1)

            can_close = can_close[can_close]
            if len(can_close) == 0:
                return None
            
            # None が 'None' に変換されてしまうことに注意。
            close_time = can_close.index[0]
            return close_time
            
        return _specify