from frestu.agent.trader.strategy.cross import StrategyDbmaReverse


class StrategyMacdReverse(StrategyDbmaReverse):

    def __init__(self, window_shorter, window_longer):
        super().__init__('ema', window_shorter, 'ema', window_longer)