from abc import abstractmethod, ABC


class PositionSizeCalculatorAbstract(ABC):

    @abstractmethod
    def __init__(self):
        pass
    
    def set_positions_size(self, positions, df):
        positions_size = self.calculate(positions, df)
        for position in positions:
            opening_time = position.opening_time
            # nan が代入されることもあることに留意
            position.position_size = positions_size.loc[opening_time][0]

    @abstractmethod
    def calculate(self, positions, df):
        pass