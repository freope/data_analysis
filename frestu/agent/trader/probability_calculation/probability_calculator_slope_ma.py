from frestu.agent.trader.probability_calculation import ProbabilityCalculatorAbstract


class ProbabilityCalculatorSlopeMa(ProbabilityCalculatorAbstract):

    def __init__(self, window_slope, sigmoid_a):
        super().__init__(sigmoid_a)
        self.__window_slope = window_slope
    
    def calculate(self, df):
        '''
        NOTE: 傾きの移動平均は、rolling を使う以下と同じ処理を、rolling を使わずに書ける。
        >>> diff = df - df.shift(1)
        >>> ma_slope = diff.rolling(self.__window_slope).mean()
        '''
        # 傾きの移動平均
        diff = df - df.shift(self.__window_slope)
        ma_slope = diff / self.__window_slope
        
        probabilities = ((self._sigmoid(ma_slope) - 0.5) * 2).abs()
        return probabilities