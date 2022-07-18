from frestu.agent.trader.strategy.cross import StrategyDbmaRaw


class StrategyMadcRaw(StrategyDbmaRaw):

    def __init__(self, window_shorter, window_longer):
        super().__init__('ema', window_shorter, 'sma', window_longer)