from frestu.optimization.agent.trader.strategy.period.spectrum import OptimizerStrategyRegularInterval as OptimizerParent


class OptimizerStrategyRegularIntervalTakeProfit(OptimizerParent):

    def __init__(self, windows, params_default, taking_rate):
        super().__init__(windows, params_default)
        self.__taking_rate = taking_rate

    def _adapt_params_to_evaluate(self, params):
        params['taking_rate'] = self.__taking_rate
        return params