from frestu.agent.trader.strategy.cross import StrategyDbmaRaw


class StrategyGccdThresholdRaw(StrategyDbmaRaw):

    def __init__(self, window_shorter, window_longer, threshold):
        super().__init__(
            'sma', window_shorter, 'ema', window_longer, threshold, -threshold)