import pandas as pd

from frestu.agent.trader.probability_calculation import ProbabilityCalculatorAbstract


class ProbabilityCalculatorUniform(ProbabilityCalculatorAbstract):

    def __init__(self, probability):
        self.__probability = probability
    
    def calculate(self, df):
        probs = pd.DataFrame([], columns=['probability'], index=df.index)
        probs.loc[:, 'probability'] = self.__probability
        return probs