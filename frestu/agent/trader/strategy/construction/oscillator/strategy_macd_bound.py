from frestu.agent.trader.strategy.construction.cross import StrategyDbmaBoundedClose


class StrategyMacdBound(StrategyDbmaBoundedClose):

    def __init__(self, window_shorter, window_longer, bound):
        super().__init__(
            'ema', window_shorter, 'ema', window_longer, bound, -bound)