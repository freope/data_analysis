import pickle

from sklearn.linear_model import Lasso

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorRaw
from frestu.feature_extraction.time_series.prediction import ExtractorPrediction
from frestu.feature_extraction.time_series import ExtractorMakingPastsNan
from frestu.feature_extraction.time_series import ExtractorFuture
from frestu.feature_selection import SelectorEachColumn
from frestu.model_selection.split_data_frame import SplitterNumber


class StrategyCrossLassoRawSkip(StrategyCrossIndicatorRaw):

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
            predictor = Lasso(alpha)
        else:
            # path_model が引数に必要
            with open(path_model, 'rb') as f:
                predictor = pickle.load(f)

        extractor = ExtractorPrediction(
            extractor_future, selector, splitter, predictor, can_fit)

        # 本番では、直近の future_shift ステップはすでに過ぎ去った扱いになってしまうため、
        # train データより新しいデータのうち、古い方から future_shift の数だけ
        # nan で埋める。
        extractor = ExtractorMakingPastsNan(
            extractor, n_data_train + future_shift)
        
        strategy = cls(extractor, col_indicator, col_raw, *args, **kwargs)

        return strategy