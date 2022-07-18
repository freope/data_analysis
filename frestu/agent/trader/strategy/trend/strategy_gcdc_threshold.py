from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyGcdcThreshold(StrategyDbma):

    def __init__(self, window_shorter, window_longer, threshold):
        super().__init__(
            'sma', window_shorter, 'sma', window_longer, threshold, -threshold)