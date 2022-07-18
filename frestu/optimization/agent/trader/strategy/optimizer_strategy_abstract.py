from abc import abstractmethod

from frestu.optimization import OptimizerAbstract


class OptimizerStrategyAbstract(OptimizerAbstract):
    
    def __init__(self):
        super().__init__()
        self.evaluate = None
        self.features = None
        self.params = None

    def optimize(self, df):
        self.features = self._calculate_features(df)
        self.params = self._calculate_the_best_params(self.features)
        self.notify_observers()

    @abstractmethod
    def _calculate_features(self, df):
        pass

    @abstractmethod
    def _calculate_the_best_params(self, features):
        pass
    
    def _adapt_params_to_evaluate(self, params):
        return params