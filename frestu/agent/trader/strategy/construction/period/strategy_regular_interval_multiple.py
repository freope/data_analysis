from frestu.agent.trader.strategy.combination import StrategyCombinatorWithAnd
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyRegularIntervalMultiple(StrategyConstructorAbstract):

    def __init__(self, periods_half, offsets, ix_close=0):
        strategies = [
            StrategyRegularInterval(period_half, offset)
            for period_half, offset in zip(periods_half, offsets)]
        strategy_open = StrategyCombinatorWithAnd(strategies)
        strategy_close = StrategyRegularInterval(
            periods_half[ix_close], offsets[ix_close])
        self._strategy = StrategyCombinatorOpenAndClose(
            strategy_open, strategy_close)