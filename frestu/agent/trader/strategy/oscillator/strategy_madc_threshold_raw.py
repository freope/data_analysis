from frestu.agent.trader.strategy.cross import StrategyDbmaRaw


class StrategyMadcThresholdRaw(StrategyDbmaRaw):

    def __init__(self, window_shorter, window_longer, threshold):
        super().__init__(
            'ema', window_shorter, 'sma', window_longer, threshold, -threshold)