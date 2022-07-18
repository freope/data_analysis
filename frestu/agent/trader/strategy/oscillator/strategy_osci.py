from frestu.agent.trader.strategy.cross import StrategyDfmaDbma


class StrategyOsci(StrategyDfmaDbma):
    """
    OSCI
    """

    def __init__(self, window, window_shorter, window_longer):
        super().__init__(
            'ema', window, 'ema', window_shorter, 'ema', window_longer)