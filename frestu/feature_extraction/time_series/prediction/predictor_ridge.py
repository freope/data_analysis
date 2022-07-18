from sklearn.linear_model import Ridge

from frestu.feature_extraction.time_series.prediction import PredictorAbstract


class PredictorRidge(PredictorAbstract):
    """
    Notes
    -----
    開発用。実際には Ridge を Predictor として直接使える。
    """

    def __init__(self, alpha):
        self.__model = Ridge(alpha)
    
    def predict(self, X):
        return self.__model.predict(X)
    
    def fit(self, X, y):
        self.__model.fit(X, y)
    
    def partial_fit(self, X, y):
        self.fit(X, y)