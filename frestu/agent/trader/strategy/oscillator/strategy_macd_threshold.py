from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyMacdThreshold(StrategyDbma):

    def __init__(self, window_shorter, window_longer, threshold):
        super().__init__(
            'ema', window_shorter, 'ema', window_longer, threshold, -threshold)