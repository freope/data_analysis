from frestu.optimization.agent.trader.strategy.period.spectrum import OptimizerStrategyRegularInterval


class OptimizerStrategyRegularIntervalStopLoss(OptimizerStrategyRegularInterval):

    def __init__(self, windows, params_default, stopping_rate):
        super().__init__(windows, params_default)
        self.__stopping_rate = stopping_rate

    def _adapt_params_to_evaluate(self, params):
        params['stopping_rate'] = self.__stopping_rate
        return params