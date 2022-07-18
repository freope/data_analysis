from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.period import StrategyRegularInterval
from frestu.agent.trader.strategy.period import StrategyRegularIntervalAndCurvature


class StrategyRegularIntervalOpenAndCurvature(StrategyConstructorAbstract):
    
    def __init__(
            self,
            period_half, offset_open, offset_close, ma_type, window,
            window_slope=1, window_curvature=1,
            threshold_long=0, threshold_short=0):
        strategy_open = StrategyRegularIntervalAndCurvature(
            period_half, offset_open, ma_type, window,
            window_slope, window_curvature, threshold_long, threshold_short)
        strategy_close = StrategyRegularInterval(period_half, offset_close)
        self._strategy = StrategyCombinatorOpenAndClose(
            strategy_open, strategy_close)