import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract


class StrategyRegularInterval(StrategyContinuousIndicatorAbstract):

    def __init__(self, period_half, offset):
        super().__init__()
        self.__period_half = period_half
        self.__offset = offset

    def calculate_open_indicators(self, df):
        boolean = False
        n_rows = df.shape[0]
        n_periods_half = (n_rows - self.__offset) // self.__period_half + 1

        indicator = np.repeat(boolean, self.__offset)

        for _ in range(n_periods_half):
            boolean = not(boolean)
            indicator = np.append(
                indicator, np.repeat(boolean, self.__period_half))

        indicator = pd.Series(indicator[:n_rows])
        indicator.index = df.index

        return indicator

    def convert_open_indicators(self, indicators, position_type):
        if position_type == 'long':
            # indicators の 1 行目を False にして、
            # opening_times と closing_times の個数を対応させる。
            indicators[0] = False
            return pd.Series(indicators)
        elif position_type == 'short':
            indicators = indicators == False
            # indicators の 1 行目を False にして、
            # opening_times と closing_times の個数を対応させる。
            indicators[0] = False
            return pd.Series(indicators)