from frestu.agent.trader.probability_calculation import ProbabilityCalculatorMaSlopeMa


class ProbabilityCalculatorMaSlope(ProbabilityCalculatorMaSlopeMa):

    def __init__(self, ma_type, window_ma, sigmoid_a):
        window_slope = 1
        super().__init__(ma_type, window_ma, window_slope, sigmoid_a)