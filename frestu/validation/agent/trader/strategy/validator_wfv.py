import os

from frestu.validation.agent.trader.strategy import Validator


class ValidatorWfv(Validator):
    
    def __init__(self, validator):
        self.__validator = validator

    def fit(self, df, span_fitting, dpath):
        self.__validator.fit(df, span_fitting, dpath)
    
    def predict(self, df, spans_pred, dpath):
        self.__validator.predict(df, spans_pred, dpath)

    def validate(self, df, spans_fitting, spans_preds, dpath):
        for span_fitting, spans_pred in zip(spans_fitting, spans_preds):
            dpath_child = os.path.join(
                dpath, self.__class__.dname_child(span_fitting))
            os.makedirs(dpath_child, exist_ok=True)
            self.fit(df, span_fitting, dpath_child)
            # self.population は、patience でストップした時のものであることに注意。
            self.predict(df, spans_pred, dpath_child)
    
    @staticmethod
    def dname_child(span_fitting, sep='_'):
        width = max(len(str(span_fitting[0])), len(str(span_fitting[1])))
        fmt = '{0:>0' + str(width) + '}' + sep + '{1:>0' + str(width) + '}'
        return fmt.format(span_fitting[0], span_fitting[1])