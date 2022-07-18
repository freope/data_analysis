from abc import abstractmethod, ABC


class ValidatorAbstract(ABC):

    @abstractmethod
    def fit(self, df, span_fitting, dpath):
        pass
    
    @abstractmethod
    def predict(self, df, spans_pred, dpath):
        pass
    
    @abstractmethod
    def validate(self, df, spans_fitting, spans_pred, dpath):
        pass