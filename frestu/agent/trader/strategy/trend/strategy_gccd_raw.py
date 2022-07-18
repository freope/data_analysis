from frestu.agent.trader.strategy.cross import StrategyDbmaRaw


class StrategyGccdRaw(StrategyDbmaRaw):

    def __init__(self, window_shorter, window_longer):
        super().__init__('sma', window_shorter, 'ema', window_longer)