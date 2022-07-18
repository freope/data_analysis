from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.combination import StrategyCombinatorEarlyClose
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.part import StrategyPartStopLossRatio
from frestu.agent.trader.strategy.trend import StrategyGcdc


class StrategyGcdcStopLossRatio(StrategyConstructorAbstract):

    def __init__(self, window_shorter, window_longer, stopping_ratio):
        strategy = StrategyGcdc(window_shorter, window_longer)
        stop_loss = StrategyPartStopLossRatio(stopping_ratio)
        early_close = StrategyCombinatorEarlyClose(strategy, stop_loss)
        self._strategy = StrategyCombinatorOpenAndClose(strategy, early_close)