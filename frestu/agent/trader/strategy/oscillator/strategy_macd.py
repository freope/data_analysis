from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyMacd(StrategyDbma):
    """
    MACD
    """

    def __init__(self, window_shorter, window_longer):
        super().__init__('ema', window_shorter, 'ema', window_longer)