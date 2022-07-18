import pickle

from sklearn.linear_model import Ridge

from frestu.agent.trader.strategy.cross import StrategyCrossIndicatorRaw
from frestu.data_type.data_frame import DataFrame
from frestu.feature_extraction.time_series.prediction import ExtractorPrediction
from frestu.feature_extraction.time_series import ExtractorFuture
from frestu.feature_selection import SelectorEachColumn
from frestu.model_selection.split_data_frame import SplitterNumber


class StrategyCrossRidgeRawGev(StrategyCrossIndicatorRaw):
    """
    Notes
    -----
    StrategyCrossRidgeRaw Gnerating Explanatory Variables
    実運営用。その場で説明変数を生成する。
    """

    def __init__(
            self,
            past_max, step_past,
            extractor, col_indicator, col_raw,
            threshold_long=0, threshold_short=0):
        super().__init__(
            extractor, col_indicator, col_raw, threshold_long, threshold_short)
        self.__past_max = past_max
        self.__step_past = step_past
        self.__col_raw = col_raw

    def calculate_open_indicators(self, df):
        # 説明変数を生成
        df = DataFrame(df).add_cols_past(
            columns=[self.__col_raw],
            shifts=range(self.__step_past, self.__past_max, self.__step_past)
        ).dropna()
        feature = super().calculate_open_indicators(df)
        return feature

    @classmethod
    def create(
            cls,
            past_max, step_past,
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
        
        strategy = cls(
            past_max, step_past,
            extractor, col_indicator, col_raw, *args, **kwargs)

        return strategy