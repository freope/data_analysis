from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.combination import StrategyCombinatorSimultaneousOpen
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract as StrategyParent
from frestu.agent.trader.strategy.construction.period import StrategyRegularIntervalOpenAndReverseSlope
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyRegularIntervalOpenAndReverseSlopeSimultaneous(StrategyParent):

    def __init__(
            self,
            time_buffer,
            period_half, offset_open, offset_close, ma_type, window,
            window_slope=1, threshold_long=0, threshold_short=0):
        strategy_0 = StrategyRegularIntervalOpenAndReverseSlope(
            period_half, offset_open, offset_close, ma_type, window,
            window_slope, threshold_long, threshold_short)
        strategy_1 = StrategyRegularInterval(period_half, offset_open)
        strategy_open = StrategyCombinatorSimultaneousOpen(
            time_buffer, strategy_0, strategy_1)
        self._strategy = StrategyCombinatorOpenAndClose(
            strategy_open, strategy_0)