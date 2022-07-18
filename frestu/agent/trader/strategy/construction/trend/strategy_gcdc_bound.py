from frestu.agent.trader.strategy.construction.cross import StrategyDbmaBoundedClose


class StrategyGcdcBound(StrategyDbmaBoundedClose):
    
    def __init__(self, window_shorter, window_longer, bound):
        super().__init__(
            'sma', window_shorter, 'sma', window_longer, bound, -bound)