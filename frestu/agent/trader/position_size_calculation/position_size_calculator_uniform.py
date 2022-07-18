import pandas as pd

from frestu.agent.trader.position_size_calculation import PositionSizeCalculatorAbstract


class PositionSizeCalculatorUniform(PositionSizeCalculatorAbstract):

    def __init__(self, position_size):
        self.__position_size = position_size

    def calculate(self, positions, df):
        positions_size = pd.DataFrame(
            [], columns=['position_size'], index=df.index)
        # ここで整数値に限定している
        positions_size.loc[:, 'position_size'] = round(self.__position_size)
        return positions_size