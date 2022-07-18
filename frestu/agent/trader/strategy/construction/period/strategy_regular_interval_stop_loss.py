from frestu.agent.trader.strategy.combination import StrategyCombinatorEarlyClose
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.part import StrategyPartStopLoss
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyRegularIntervalStopLoss(StrategyConstructorAbstract):

    def __init__(self, period_half, offset, stopping_rate):
        strategy = StrategyRegularInterval(period_half, offset)
        stop_loss = StrategyPartStopLoss(stopping_rate)
        early_close = StrategyCombinatorEarlyClose(strategy, stop_loss)
        self._strategy = StrategyCombinatorOpenAndClose(strategy, early_close)