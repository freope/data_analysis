import numpy as np
import pandas as pd

from frestu.agent.trader.position_size_calculation import PositionSizeCalculatorAbstract


class PositionSizeCalculatorLinear(PositionSizeCalculatorAbstract):

    def __init__(self, position_size_max):
        self.__position_size_max = position_size_max
    
    def calculate(self, positions, df):
        positions_size = []
        for position in positions:
            opening_time = position.opening_time
            probability = position.probability

            # nan が代入されることもあることに留意
            if np.isnan(probability):
                position_size = np.nan
            else:
                # ここで整数値に限定している
                position_size = round(self.__position_size_max * probability)

            positions_size.append({
                'time': opening_time,
                'position_size': position_size})

        # positions が空の場合、set_time('time') でエラーになるため。
        # set_positions_size() の for が回らないので何も返さなくて問題ない。
        if len(positions_size) == 0:
            return

        positions_size = pd.DataFrame(positions_size).set_index('time')
        return positions_size