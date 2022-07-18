from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyMacdThresholds(StrategyDbma):

    def __init__(
            self,
            window_shorter, window_longer,
            threshold_long, threshold_short):
        super().__init__(
            'ema', window_shorter, 'ema', window_longer,
            threshold_long, -threshold_short)