from frestu.agent.trader.strategy.construction.cross import StrategyDbmaBoundedClose


class StrategyMacdBounds(StrategyDbmaBoundedClose):

    def __init__(self, window_shorter, window_longer, bound_long, bound_short):
        super().__init__(
            'ema', window_shorter, 'ema', window_longer,
            bound_long, -bound_short)