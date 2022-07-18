from abc import abstractmethod, ABC

import numpy as np


class ProbabilityCalculatorAbstract(ABC):

    def __init__(self, sigmoid_a):
        self.__sigmoid_a = sigmoid_a

    def set_positions_probability(self, positions, df):
        probabilities = self.calculate(df)
        for position in positions:
            opening_time = position.opening_time
            # nan が代入されることもあることに留意
            position.probability = probabilities.loc[opening_time][0]

    @abstractmethod
    def calculate(self, df):
        pass

    def _sigmoid(self, x):
        return 1 / (1 + np.exp(-self.__sigmoid_a * x))