from frestu.agent.trader.strategy.combination import StrategyCombinatorEarlyClose
from frestu.agent.trader.strategy.combination import StrategyCombinatorOpenAndClose
from frestu.agent.trader.strategy.construction import StrategyConstructorAbstract as StrategyParent
from frestu.agent.trader.strategy.part import StrategyPartStopLoss
from frestu.agent.trader.strategy.part import StrategyPartTakeProfit
from frestu.agent.trader.strategy.period import StrategyRegularInterval


class StrategyOpenRegularIntervalCloseTakeProfitStopLoss(StrategyParent):

    def __init__(self, period_half, offset, taking_rate, stopping_rate):
        strategy = StrategyRegularInterval(period_half, offset)
        take_profit = StrategyPartTakeProfit(taking_rate)
        stop_loss = StrategyPartStopLoss(stopping_rate)
        early_close = StrategyCombinatorEarlyClose(take_profit, stop_loss)
        self._strategy = StrategyCombinatorOpenAndClose(strategy, early_close)