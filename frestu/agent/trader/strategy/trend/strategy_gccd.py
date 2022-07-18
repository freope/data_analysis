from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyGccd(StrategyDbma):

    def __init__(self, window_shorter, window_longer):
        super().__init__('sma', window_shorter, 'ema', window_longer)