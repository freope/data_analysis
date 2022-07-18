from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.combination import StrategyCombinatorWithAnd
from frestu.agent.trader.strategy.trend import StrategyGcdc
from frestu.agent.trader.strategy.trend import StrategyMau


class StrategyGcdcAndMau(StrategyConstructorAbstract):

    def __init__(self, window_shorter, window_longer, windows):
        gcdc = StrategyGcdc(window_shorter, window_longer)
        mau = StrategyMau(windows)
        strategies = [gcdc, mau]
        self._strategy = StrategyCombinatorWithAnd(strategies)
