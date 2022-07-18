from datetime import datetime as dt

import numpy as np
import pandas as pd

from frestu.agent.trader.strategy import StrategyAbstract


class StrategyCombinatorEarlyClose(StrategyAbstract):
    
    def __init__(self, strategy_0, strategy_1):
        super().__init__()
        self.__strategy_0 = strategy_0
        self.__strategy_1 = strategy_1

    def calculate_opening_times(self, df):
        pass
    
    def calculate_closing_times(self, df, opening_times):
        closing_times_0 = self.__strategy_0.calculate_closing_times(
            df, opening_times)
        closing_times_1 = self.__strategy_1.calculate_closing_times(
            df, opening_times)

        # long
        closing_times_long = self.__calculate_earlier_closing_times(
            closing_times_0[0], closing_times_1[0])

        # short
        closing_times_short = self.__calculate_earlier_closing_times(
            closing_times_0[1], closing_times_1[1])

        return closing_times_long, closing_times_short

    def calculate_times(self, df):
        pass

    def __calculate_earlier_closing_times(
            self, closing_times_0, closing_times_1):
        closing_times_0 = pd.DataFrame(closing_times_0)
        closing_times_1 = pd.DataFrame(closing_times_1)

        # 片方が None の場合は、もう片方の値を採用
        closing_times_0 = closing_times_0.fillna(closing_times_1)
        closing_times_1 = closing_times_1.fillna(closing_times_0)

        # 両方とも None の場合は、後の処理の dropna で建玉の None が
        # 消えてしまうので、一旦 True に置き換える
        closing_times_0 = closing_times_0.fillna(True)
        closing_times_1 = closing_times_1.fillna(True)

        is_earlier_0 = closing_times_0 < closing_times_1
        closing_times = closing_times_0[is_earlier_0].fillna(
            closing_times_1[~is_earlier_0])

        closing_times = closing_times.mask(closing_times == True, None)

        # 空だと iloc[:, 0] でエラーが出るので。
        if closing_times.shape[0] == 0:
            return np.array([])

        closing_times = np.array(closing_times.iloc[:, 0])

        return closing_times
