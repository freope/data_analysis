from frestu.agent.trader.probability_calculation import ProbabilityCalculatorAbstract
from frestu.feature_extraction.time_series import ExtractorMa


class ProbabilityCalculatorMaSlopeMa(ProbabilityCalculatorAbstract):

    def __init__(self, ma_type, window_ma, window_slope, sigmoid_a):
        super().__init__(sigmoid_a)
        self.__extractor = ExtractorMa(ma_type, window_ma)
        self.__window_slope = window_slope
    
    def calculate(self, df):
        ma = self.__extractor.extract(df)

        # 移動平均の傾きの移動平均
        diff_ma = ma - ma.shift(self.__window_slope)
        ma_slope = diff_ma / self.__window_slope

        probabilities = ((self._sigmoid(ma_slope) - 0.5) * 2).abs()
        return probabilities
