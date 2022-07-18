from abc import abstractmethod, ABC


class PredictorAbstract(ABC):

    @abstractmethod
    def predict(self):
        pass
    
    @abstractmethod
    def fit(self):
        pass
    
    @abstractmethod
    def partial_fit(self):
        pass