from frestu.agent.trader.strategy.construction.cross import StrategyDbmaBoundedClose


class StrategyMacdBoundThreshold(StrategyDbmaBoundedClose):

    def __init__(self, window_shorter, window_longer, bound, threshold):
        super().__init__(
            'ema', window_shorter, 'ema', window_longer,
            bound, -bound, threshold, -threshold)