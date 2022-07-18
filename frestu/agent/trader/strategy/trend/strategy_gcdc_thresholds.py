from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyGcdcThresholds(StrategyDbma):

    def __init__(
            self,
            window_shorter, window_longer,
            threshold_long, threshold_short):
        super().__init__(
            'sma', window_shorter, 'sma', window_longer,
            threshold_long, -threshold_short)