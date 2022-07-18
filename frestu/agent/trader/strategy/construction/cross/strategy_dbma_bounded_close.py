from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.cross import StrategyDbmaBounded
from frestu.agent.trader.strategy.cross import StrategyDbma


class StrategyDbmaBoundedClose(StrategyConstructorAbstract):

    def __init__(
            self,
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            bound_long, bound_short,
            threshold_long=0, threshold_short=0):
        strategy_open = StrategyDbma(
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            threshold_long, threshold_short)
        strategy_close = StrategyDbmaBounded(
            ma_type_shorter, window_shorter,
            ma_type_longer, window_longer,
            bound_long, bound_short,
            threshold_long, threshold_short)
        self._strategy = StrategyCombinatorOpenAndClose(
            strategy_open, strategy_close)