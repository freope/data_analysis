import os

from frestu.evaluation import ObserverEvaluatorAbstract


class ObserverSaverTrader(ObserverEvaluatorAbstract):

    def __init__(
            self,
            pop_size,
            i_top_saved,
            dpath,
            fname_prefix='positions_'):
        self.__pop_size = pop_size
        self.__dpath = dpath
        self.__i_top_saved = i_top_saved
        self.__fname_prefix = fname_prefix
        self.__i_trader = 0
        self.__span_traders = []
        self.spans_traders = []

    def observe(self, evaluator):
        trader = evaluator.trader
        self.__i_trader += 1
        self.__span_traders.append(trader)
        if self.__i_trader % self.__pop_size == 0:
            fname = f'{self.__fname_prefix}{self.__i_trader}.csv'
            self.__span_traders[self.__i_top_saved].history.to_csv(
                os.path.join(self.__dpath, fname))
            
            self.spans_traders.append(self.__span_traders)
            self.__span_traders = []