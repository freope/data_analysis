from frestu.agent.trader.strategy.combination import StrategyCombinatorEarlyClose
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.part import StrategyPartTakeProfit
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyRegularIntervalTakeProfit(StrategyConstructorAbstract):

    def __init__(self, period_half, offset, taking_rate):
        strategy = StrategyRegularInterval(period_half, offset)
        take_profit = StrategyPartTakeProfit(taking_rate)
        early_close = StrategyCombinatorEarlyClose(strategy, take_profit)
        self._strategy = StrategyCombinatorOpenAndClose(strategy, early_close)