from frestu.agent.trader.strategy.construction.cross import StrategyDbmaBoundedClose


class StrategyGcdcBounds(StrategyDbmaBoundedClose):
    
    def __init__(self, window_shorter, window_longer, bound_long, bound_short):
        super().__init__(
            'sma', window_shorter, 'sma', window_longer,
            bound_long, -bound_short)