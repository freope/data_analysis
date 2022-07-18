from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.cross import StrategyDfmaBounded
from frestu.agent.trader.strategy.cross import StrategyDfma


class StrategyDfmaBoundedClose(StrategyConstructorAbstract):

    def __init__(
            self,
            ma_type, window,
            bound_long, bound_short,
            threshold_long=0, threshold_short=0):
        strategy_open = StrategyDfma(
            ma_type, window, threshold_long, threshold_short)
        strategy_close = StrategyDfmaBounded(
            ma_type, window,
            bound_long, bound_short,
            threshold_long, threshold_short)
        self._strategy = StrategyCombinatorOpenAndClose(
            strategy_open, strategy_close)