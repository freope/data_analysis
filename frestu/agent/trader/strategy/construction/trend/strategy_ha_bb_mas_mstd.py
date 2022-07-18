from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract
from frestu.agent.trader.strategy.combination import StrategyCombinatorWithAnd
from frestu.agent.trader.strategy.trend import StrategyHeikinashi
from frestu.agent.trader.strategy.trend import StrategyBbMasMstd


class StrategyHaBbMasMstd(StrategyConstructorAbstract):

    def __init__(self, window_ha, threshold, ma_type, window_bb):
        strategy_ha = StrategyHeikinashi(window_ha)
        strategy_bb = StrategyBbMasMstd(threshold, ma_type, window_bb)
        strategies = [strategy_ha, strategy_bb]
        self._strategy = StrategyCombinatorWithAnd(strategies)