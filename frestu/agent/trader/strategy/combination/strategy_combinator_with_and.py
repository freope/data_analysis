import pandas as pd

from frestu.agent.trader.strategy import StrategyContinuousIndicatorAbstract


class StrategyCombinatorWithAnd(StrategyContinuousIndicatorAbstract):

    def __init__(self, strategies):
        """
        複数の戦略を AND 結合で連結させた戦略を生成する。

        Parameters
        ----------
        strategies : list of strategy
            戦略を要素に持つリスト
        """
        super().__init__()
        self.__strategies = strategies

    def calculate_open_indicators(self, df):
        can_open_long = []
        can_open_short = []
        for strategy in self.__strategies:
            indicator = strategy.calculate_open_indicators(df)
            can_open_long.append(strategy.convert_open_indicators(
                indicator, position_type='long'))
            can_open_short.append(strategy.convert_open_indicators(
                indicator, position_type='short'))
        can_open_long = pd.concat(can_open_long, axis=1).all(axis=1)
        can_open_short = pd.concat(can_open_short, axis=1).all(axis=1)
        can_open = pd.concat([can_open_long, can_open_short], axis=1)
        can_open.columns = ['long', 'short']
        return can_open

    def convert_open_indicators(self, indicators, position_type):
        return indicators[position_type]