import pickle

from sklearn.linear_model import Ridge

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorRaw
from frestu.feature_extraction.time_series.prediction import ExtractorPrediction
from frestu.feature_extraction.time_series import ExtractorFuture
from frestu.feature_selection import SelectorEachColumn
from frestu.model_selection.split_data_frame import SplitterNumber


class StrategyCrossRidgeRaw(StrategyCrossIndicatorRaw):

    @classmethod
    def create(
            cls,
            future_shift, zerones, n_data_train, col_indicator, col_raw,
            can_fit, alpha=None, path_model=None, *args, **kwargs):
        extractor_future = ExtractorFuture(future_shift, col_raw, col_indicator)
        selector = SelectorEachColumn(zerones)
        splitter = SplitterNumber(n_data_train, col_indicator)

        if can_fit:
            # alpha が引数に必要
            predictor = Ridge(alpha)
        else:
            # path_model が引数に必要
            with open(path_model, 'rb') as f:
                predictor = pickle.load(f)

        extractor = ExtractorPrediction(
            extractor_future, selector, splitter, predictor, can_fit)
        
        strategy = cls(extractor, col_indicator, col_raw, *args, **kwargs)

        return strategy